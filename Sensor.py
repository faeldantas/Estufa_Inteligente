import socket
import time
import json

TIMEOUT_INTERVAL = 5  # Intervalo de tempo em segundos entre leituras de dados

class Sensor:
    def __init__(self, sensor_id, name, ambiente, server_host='127.0.0.1', server_port=9999, ready_event=None):
        self.sensor_id = sensor_id
        self.name = name
        self.ambiente = ambiente
        self.server_host = server_host
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready_event = ready_event 
    

    def connect_to_server(self):
        """Tenta conectar ao servidor."""
        try:
            print(f"{self.name} tentando conectar ao servidor...\n")
            if self.ready_event:
                print(f"{self.name} esperando o servidor estar pronto...\n")
                self.ready_event.wait()
            self.client.connect((self.server_host, self.server_port))
            print(f"{self.name} conectado ao servidor.")
        except socket.error as e:
            print(f"Erro ao conectar ao servidor: {e}")
            self.client.close()


    def construct_message(self):
        """Constrói a mensagem com base no tipo de sensor."""
        if self.sensor_id == "TI001":
            return {"sensor": self.name, "type": "temperatura", "value": self.ambiente.get_temperatura()}
        elif self.sensor_id == "US002":
            return {"sensor": self.name, "type": "umidade", "value": self.ambiente.get_umidade()}
        else:
            return {"sensor": self.name, "type": "co2", "value": self.ambiente.get_co2()}
        

    def receive_response(self):
        """Recebe a resposta do servidor."""
        try:
            response = self.client.recv(1024).decode('utf-8')
            print(f"Recebido do servidor: {response}")
        except socket.timeout:
            print("Timeout ao receber resposta do servidor.")


    def send_data(self):
        """Envia dados periodicamente ao servidor."""
        try:
            while True:
                data = self.construct_message()
                message = json.dumps(data) + "\n"
                self.client.send(message.encode('utf-8'))
                self.receive_response()
                time.sleep(TIMEOUT_INTERVAL) 
        except Exception as e:
            print(f"Erro no sensor {self.name}: {e}")
            self.client.close()


    def run(self):
        """Executa o sensor."""
        self.connect_to_server()
        self.send_data()
