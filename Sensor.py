import socket
import time
import multiprocessing

class Sensor:
    def __init__(self, server_host='127.0.0.1', server_port=9999, ready_event=None, name=None):
        self.server_host = server_host
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready_event = ready_event
        self.sensor_name = name
    
    def connect(self):
        if self.ready_event:
            self.ready_event.wait()  # Espera até o servidor estar pronto
        self.client.connect((self.server_host, self.server_port))

    def send_data(self):
        try:
            while True:
                sensor_data = f"{self.name}: Dados do sensor (ex: temperatura=25)"
                self.client.send(sensor_data.encode('utf-8'))
                response = self.client.recv(1024).decode('utf-8')
                print(f"Received from server: {response}")
                time.sleep(5)  # Simular leitura de dados a cada 5 segundos
        except:
            self.client.close()

    def run(self):
        print("Running sensor...")
        self.connect()
        self.send_data()
