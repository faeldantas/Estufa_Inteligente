import socket
import time
import threading
import random


class Sensor:
    def __init__(self, name, ambiente, server_host='127.0.0.1', server_port=9999, ready_event=None):
        self.name = name
        self.ambiente = ambiente
        self.server_host = server_host
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready_event = ready_event
    
    def connect(self):
        if self.ready_event:
            print(f"{self.name} is waiting for the server to be ready.")
            self.ready_event.wait()  # Espera até o servidor estar pronto
        print(f"{self.name} is connecting to the server.")
        self.client.connect((self.server_host, self.server_port))

    def send_data(self):
        try:
            while True:
                if self.name == "Sensor de Temperatura":
                    sensor_data = f"{self.name}: temperatura={self.ambiente.get_temperatura()}C"
                elif self.name == "Sensor de Umidade":
                    sensor_data = f"{self.name}: umidade={self.ambiente.get_umidade()}%"
                else:
                    sensor_data = f"{self.name}: co2={self.ambiente.get_co2()} ppm"
                
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


class Sensor_temp(Sensor):
    def __init__(self, name, ambiente, server_host='127.0.0.1', server_port=9999, ready_event=None):
        super().__init__(name, ambiente, server_host, server_port, ready_event)
        

class Sensor_umid(Sensor):
    def __init__(self, name, ambiente, server_host='127.0.0.1', server_port=9999, ready_event=None):
        super().__init__(name, ambiente, server_host, server_port, ready_event)
        