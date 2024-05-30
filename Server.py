import socket
import threading
import time
import json
import select

class ServerManager:
    def __init__(self, ambiente, host='127.0.0.1', port=9999, ready_event=None):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.client_sockets = []
        self.ready_event = ready_event
        self.ambiente = ambiente


    def handle_client(self, client_socket, addr):
        #print(f"Accepted connection from {addr}")
        self.clients.append((client_socket, addr))
        self.client_sockets.append(client_socket)
        try:
            buffer = ""
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    try:
                        sensor_data = json.loads(line)
                        print(f"Recebido de {sensor_data['sensor']}: {sensor_data['type']} = {sensor_data['value']}")
                        if sensor_data['type'] == 'temperatura':
                            response = "Comando para temperatura"
                        elif sensor_data['type'] == 'umidade':
                            response = "Comando para esguicho"
                        else:
                            response = "Comando para atuador"
                        client_socket.send(response.encode('utf-8'))
                    except json.JSONDecodeError as e:
                        print(f"Erro ao decodificar JSON: {e}")

        except Exception as e:
            print(f"Erro no cliente: {e}")

        finally:
            client_socket.close()
            self.client_sockets.remove(client_socket)
            self.clients = [c for c in self.clients if c[0] != client_socket]


    def send_command_to_all(self):
        while True:
            try:
                if self.ambiente.get_temperatura() > 25:
                    print("Temperatura acima de 25, enviando comando para reduzir temperatura.")
                    for client in self.client_sockets:
                        try:
                            #print("Enviando comando para um cliente." + '\n')
                            command = json.dumps({
                                "target": "esguicho",
                                "command": "set_temperatura",
                                "value": self.ambiente.get_temperatura() - 1
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")
                time.sleep(5)  # Esperar 5 segundos antes de enviar o próximo comando
            except Exception as e:
                print(f"Erro no envio de comando: {e}")
                break

    

    def start_server(self):
        print("Starting Server...")
        self.server.bind((self.host, self.port))
        self.server.listen(10)
        print(f"Server listening on port {self.port}")
        if self.ready_event:
            self.ready_event.set()
            print("Server is ready and listening for connections.")
        try:
            control_thread = threading.Thread(target=self.send_command_to_all)
            control_thread.start()
            # check_updates_thread = threading.Thread(target=self.check_for_updates)
            # check_updates_thread.start()

            while True:
                client_socket, addr = self.server.accept()
                # if client_socket not in self.client_sockets:
                #     self.client_sockets.append(client_socket)

                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_handler.start()
                

        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server.close()