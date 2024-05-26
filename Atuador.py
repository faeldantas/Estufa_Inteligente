import socket
import multiprocessing

class Atuador:
    def __init__(self, server_host='127.0.0.1', server_port=9999, ready_event=None, name=None):
        self.server_host = server_host
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready_event = ready_event
        self.atuador_name = name
    
    def connect(self):
        if self.ready_event:
            self.ready_event.wait()  # Espera até o servidor estar pronto
        self.client.connect((self.server_host, self.server_port))

    def listen_for_commands(self):
        try:
            while True:
                response = self.client.recv(1024).decode('utf-8')
                if response:
                    print(f"Command from server: {response}")
                    # Executar ação do atuador com base no comando recebido
        except:
            self.client.close()

    def run(self):
        self.connect()
        self.listen_for_commands()
