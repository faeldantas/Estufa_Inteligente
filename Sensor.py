import socket
import time
import threading
import random

class Sensor:
    def __init__(self, name, server_host='127.0.0.1', server_port=9999, ready_event=None):
        self.name = name
        self.server_host = server_host
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready_event = ready_event
        self.valor = random.randint(25, 30)
        self.change = [-2, -1, 0 , 1, 2]
    
    def connect(self):
        if self.ready_event:
            print(f"{self.name} is waiting for the server to be ready.")
            self.ready_event.wait()  # Espera até o servidor estar pronto
        print(f"{self.name} is connecting to the server.")
        self.client.connect((self.server_host, self.server_port))

    def send_data(self):
        try:
            while True:
                self.valor += random.choice(self.change)
                sensor_data = f"{self.name}: Dados do sensor (ex: temperatura={self.valor})"
                self.client.send(sensor_data.encode('utf-8'))
                response = self.client.recv(1024).decode('utf-8')
                print(f"Received from server: {response}")
                time.sleep(5)  # Simular leitura de dados a cada 5 segundos
        except Exception as e:
            print(f"Erro no sensor {self.name}: {e}")
            self.client.close()

    def run(self):
        self.connect()
        self.send_data()
