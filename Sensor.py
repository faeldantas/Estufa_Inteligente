import socket
import time
import threading
import json

class Sensor:
    def __init__(self, id, name, ambiente, server_host='127.0.0.1', server_port=9999, ready_event=None):
        self.id = id
        self.name = name
        self.ambiente = ambiente
        self.server_host = server_host
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready_event = ready_event
    
    def connect(self):
        if self.ready_event:
            print(f"{self.name} is waiting for the server to be ready." + "\n")
            self.ready_event.wait()  # Espera até o servidor estar pronto
        self.client.connect((self.server_host, self.server_port))
        print(f"{self.name} is connecting to the server."+ "\n")

    def send_data(self):
            try:
                while True:
                    if self.name == "Temperatura interna": #mudar para id tudo que usa nome
                        data = {"sensor": self.name, "type": "temperatura", "value": self.ambiente.get_temperatura()}
                    elif self.name == "Umidade do solo":
                        data = {"sensor": self.name, "type": "umidade", "value": self.ambiente.get_umidade()}
                    else:
                        data = {"sensor": self.name, "type": "co2", "value": self.ambiente.get_co2()}
                    
                    message = json.dumps(data) + "\n"
                    self.client.send(message.encode('utf-8'))
                    #print(f"Atualizacao de sensor enviada: {message.strip()}")
                    try:
                        response = self.client.recv(1024).decode('utf-8')
                        #print(f"Received from server: {response}")
                    except socket.timeout:
                        print("Timeout ao receber resposta do servidor.")
                    time.sleep(5)  # Simular leitura de dados a cada 5 segundos
            except Exception as e:
                print(f"Erro no sensor {self.name}: {e}")
                self.client.close()

    def run(self):
            self.connect()
            self.send_data()

class Sensor_temp(Sensor):
    def __init__(self, id, name, ambiente, server_host='127.0.0.1', server_port=9999, ready_event=None):
        super().__init__(id, name, ambiente, server_host, server_port, ready_event)

class Sensor_umid(Sensor):
    def __init__(self, id, name, ambiente, server_host='127.0.0.1', server_port=9999, ready_event=None):
        super().__init__(id, name, ambiente, server_host, server_port, ready_event)

class Sensor_co2(Sensor):
    def __init__(self, id, name, ambiente, server_host='127.0.0.1', server_port=9999, ready_event=None):
        super().__init__(id, name, ambiente, server_host, server_port, ready_event)
