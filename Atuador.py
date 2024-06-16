import socket
import threading
import json
import time

class Atuador:
    def __init__(self, id, name, ambiente, ready_event=None):
        self.id = id
        self.name = name
        self.ambiente = ambiente
        self.ready_event = ready_event
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = '127.0.0.1'
        self.server_port = 9999
        self.active = False
        self.actuating_thread = None

    def connect(self):
        try:
            print(f"{self.name} tentando conectar ao servidor...\n")
            if self.ready_event:
                print(f"{self.name} esperando o servidor estar pronto...\n")
                self.ready_event.wait()
            self.client.connect((self.server_host, self.server_port))
            print(f"{self.name} conectado ao servidor.")
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")

    #Espera comandos do servidor
    def listen_for_commands(self):
        try:
            while True:
                response = self.client.recv(1024).decode('utf-8')
                if response:
                    command = json.loads(response)
                    #print(f'Comando recebido: {command}\n')
                    if command['target'] == self.id:
                        self.execute_command(command)
                        #print('Comando executado\n')
        except Exception as e:
            print(f"Erro ao receber comando: {e}")

    #Modifica parâmetros no ambiente
    def start_actuating(self):
        while self.active:
            if self.id == "AA01":
                self.ambiente.set_temperatura(self.ambiente.get_temperatura() + 1)
            elif self.id == "AR02":
                self.ambiente.set_temperatura(self.ambiente.get_temperatura() - 1)
            elif self.id == "AI03":
                self.ambiente.set_umidade(self.ambiente.get_umidade() + 5.0)
            elif self.id == "ACO2":
                self.ambiente.set_co2(self.ambiente.get_co2() + 10)
            time.sleep(2)

    #Define rotina de acordo com o comando enviado
    def execute_command(self, command):
        action = command['command']
        value = command.get('value')
        if action == "turn_on":
            print(f"{self.name} ativado.")
            self.active = True
            if self.actuating_thread is None or not self.actuating_thread.is_alive():
                self.actuating_thread = threading.Thread(target=self.start_actuating)#As mudanças serão feitas em thread separada para melhor acoplamento e independêcia
                self.actuating_thread.start()
        elif action == "turn_off":
            print(f"{self.name} desativado.")
            self.active = False


    def run(self):
        self.connect()
        self.listen_for_commands()
