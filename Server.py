import socket
import threading
import time

class ServerManager:
    def __init__(self, ambiente, host='0.0.0.0', port=9999, ready_event=None):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.ready_event = ready_event
        self.ambiente = ambiente

    def start_server(self):
        print("Starting Server...")
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Server listening on port {self.port}")
        if self.ready_event:
            self.ready_event.set()  # Sinaliza que o servidor está pronto
            print("Server is ready and listening for connections.")
        else:
            print("Tá passando errado")

        while True:
            client_socket, addr = self.server.accept()
            self.clients.append(client_socket)
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            comand_handle = threading.Thread(target=self.send_command_to_all)
            comand_handle.start()
            client_handler.start()


    def send_command_to_all(self):
        while True:
            try:
                if self.ambiente.get_temperatura() > 25:
                    for client in self.clients:
                        command = f"temperatura={self.ambiente.get_temperatura()-1}\n"
                        client.send(command.encode('utf-8'))
                    time.sleep(5)

            except Exception as e:
                print(f"Erro no envio de comando: {e}")
                break

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Recebido: {data}")
                if "Temperatura" in data:
                    response = "Comando para temperatura"
                elif "Umidade" in data:
                    response = "Comando para esguicho"
                else:
                    response = "Comando para atuador"
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                print(f"Erro no cliente: {e}")
                break
        client_socket.close()
