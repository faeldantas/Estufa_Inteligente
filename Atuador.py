import socket
import threading
import json

class Atuador:
    def __init__(self, name, ambiente, ready_event=None):
        self.name = name
        self.ambiente = ambiente
        self.ready_event = ready_event
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = '127.0.0.1'
        self.server_port = 9999

    def connect(self):
        try:
            print(f"{self.name} tentando conectar ao servidor..." + "\n")
            if self.ready_event:
                print(f"{self.name} esperando o servidor estar pronto..." + "\n")
                self.ready_event.wait()
            self.client.connect((self.server_host, self.server_port))
            print(f"{self.name} conectado ao servidor.")
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")

    def listen_for_commands(self):
        try:
            while True:
                response = self.client.recv(1024).decode('utf-8')
                if response:
                    command = json.loads(response)
                    #print(f'Comando recebido: {command}' + '\n')
                    if command['target'] == self.name:
                        print('Comando executado' + '\n')
                        self.execute_command(command)
        except Exception as e:
            print(f"Erro ao receber comando: {e}")

    def execute_command(self, command):
        action = command['command']
        value = command.get('value')
        if action == "turn_on":
            duration = value.get('duration', 0)
            print(f"{self.name} ativado por {duration} segundos.")
            # Aqui você pode adicionar a lógica para realmente ativar o atuador
        elif action == "turn_off":
            print(f"{self.name} desativado.")
            # Aqui você pode adicionar a lógica para realmente desativar o atuador
        elif action == "set_temperatura":
            print(f"{self.name} ajustando temperatura para {value}.")
            self.ambiente.set_temperatura(value)
            # Aqui você pode adicionar a lógica para ajustar a temperatura

    def run(self):
        self.connect()
        self.listen_for_commands()
