import socket
import threading
import time
import json

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
        self.limits_set = False  # Variável para rastrear se os limites foram definidos
        self.latest_data = {"temperatura": None, "umidade": None, "co2": None}  # Armazena os últimos dados recebidos
        self.limits_condition = threading.Condition()

    def handle_client(self, client_socket, addr):
        print(f"Aceitou conexão de {addr}")
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
                        print(sensor_data)
                        if 'action' in sensor_data:
                            if sensor_data['action'] == 'get_latest_data':
                                # Cliente solicitando a última atualização dos dados
                                response = json.dumps(self.latest_data)
                                client_socket.send(response.encode('utf-8'))

                            elif sensor_data['action'] == 'define_limits':
                                print("Recebido pedido de definição de limites")
                                self.ambiente.set_limits(
                                    min_temp=sensor_data['min_temp'],
                                    max_temp=sensor_data['max_temp'],
                                    min_umid=sensor_data.get('min_umid'),
                                    max_umid=sensor_data.get('max_umid'),
                                    min_co2=sensor_data.get('min_co2'),
                                    max_co2=sensor_data.get('max_co2')
                                )
                                print("Limites do ambiente atualizados.")
                                with self.limits_condition:
                                    self.limits_set = True
                                    self.limits_condition.notify_all()
                                response = json.dumps({"status": "ok"})
                                client_socket.send(response.encode('utf-8'))

                        elif 'sensor' in sensor_data and 'type' in sensor_data and 'value' in sensor_data:
                            print(f"Recebido de {sensor_data['sensor']}: {sensor_data['type']} = {sensor_data['value']}")
                            if sensor_data['type'] == 'temperatura':
                                self.latest_data['temperatura'] = sensor_data['value']
                            elif sensor_data['type'] == 'umidade':
                                self.latest_data['umidade'] = sensor_data['value']
                            elif sensor_data['type'] == 'co2':
                                self.latest_data['co2'] = sensor_data['value']
                            response = json.dumps({"status": "ok"})
                            client_socket.send(response.encode('utf-8'))

                        else:
                            response = json.dumps({"status": "error", "message": "Invalid data format"})
                            client_socket.send(response.encode('utf-8'))
                    except json.JSONDecodeError as e:
                        print(f"Erro ao decodificar JSON: {e}")

        except Exception as e:
            print(f"Erro no cliente: {e}")

        finally:
            client_socket.close()
            self.client_sockets.remove(client_socket)
            self.clients = [c for c in self.clients if c[0] != client_socket]

    def regulate_periodically(self):
        with self.limits_condition:
            while not self.limits_set:
                print("Aguardando definição dos limites para iniciar a regulação...")
                self.limits_condition.wait()

        # Dicionário para rastrear o estado dos atuadores
        atuator_states = {
            "AR02": False,  # Resfriador inicialmente desligado
            "AA01": False,  # Aquecedor inicialmente desligado
            "AI03": False,  # Umidificador inicialmente desligado
            "ACO2": False   # Atuador de CO2 inicialmente desligado
        }

        while True:
            try:
                # Verifica Resfriador
                if self.ambiente.get_temperatura() > self.ambiente.max_temp:
                    if not atuator_states["AR02"]:
                        print(f"Temperatura acima de {self.ambiente.max_temp}, enviando comando para reduzir temperatura.")
                        for client in self.client_sockets:
                            try:
                                command = json.dumps({
                                    "target": "AR02",
                                    "command": "turn_on",
                                }) + "\n"
                                client.send(command.encode('utf-8'))
                                atuator_states["AR02"] = True  # Atualiza estado do atuador
                            except Exception as client_error:
                                print(f"Erro ao enviar comando para um cliente: {client_error}")
                elif atuator_states["AR02"]:  # Só envia "turn_off" se estiver ligado
                    for client in self.client_sockets:
                        try:
                            command = json.dumps({
                                "target": "AR02",
                                "command": "turn_off",
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                            atuator_states["AR02"] = False  # Atualiza estado do atuador
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")

                time.sleep(1)

                # Verifica Aquecedor
                if self.ambiente.get_temperatura() < self.ambiente.min_temp:
                    if not atuator_states["AA01"]:
                        print(f"Temperatura abaixo de {self.ambiente.min_temp}, enviando comando para aumenta-la.")
                        for client in self.client_sockets:
                            try:
                                command = json.dumps({
                                    "target": "AA01",
                                    "command": "turn_on",
                                }) + "\n"
                                client.send(command.encode('utf-8'))
                                atuator_states["AA01"] = True  # Atualiza estado do atuador
                            except Exception as client_error:
                                print(f"Erro ao enviar comando para um cliente: {client_error}")
                elif atuator_states["AA01"]:  # Só envia "turn_off" se estiver ligado
                    for client in self.client_sockets:
                        try:
                            command = json.dumps({
                                "target": "AA01",
                                "command": "turn_off",
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                            atuator_states["AA01"] = False  # Atualiza estado do atuador
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")

                time.sleep(1)

                # Verifica Umidade
                if self.ambiente.get_umidade() < self.ambiente.min_umid:
                    if not atuator_states["AI03"]:
                        print(f"Umidade abaixo de {self.ambiente.min_umid}%, enviando comando para aumenta-la.")
                        for client in self.client_sockets:
                            try:
                                command = json.dumps({
                                    "target": "AI03",
                                    "command": "turn_on",
                                }) + "\n"
                                client.send(command.encode('utf-8'))
                                atuator_states["AI03"] = True  # Atualiza estado do atuador
                            except Exception as client_error:
                                print(f"Erro ao enviar comando para um cliente: {client_error}")
                elif atuator_states["AI03"]:  # Só envia "turn_off" se estiver ligado
                    for client in self.client_sockets:
                        try:
                            command = json.dumps({
                                "target": "AI03",
                                "command": "turn_off",
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                            atuator_states["AI03"] = False  # Atualiza estado do atuador
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")

                time.sleep(1)

                # Verifica CO2
                if self.ambiente.get_co2() < self.ambiente.min_co2:
                    if not atuator_states["ACO2"]:
                        print("Nivel de CO2 baixo, enviando comando para aumentá-lo.")
                        for client in self.client_sockets:
                            try:
                                command = json.dumps({
                                    "target": "ACO2",
                                    "command": "turn_on",
                                }) + "\n"
                                client.send(command.encode('utf-8'))
                                atuator_states["ACO2"] = True  # Atualiza estado do atuador
                            except Exception as client_error:
                                print(f"Erro ao enviar comando para um cliente: {client_error}")
                elif atuator_states["ACO2"]:  # Só envia "turn_off" se estiver ligado
                    for client in self.client_sockets:
                        try:
                            command = json.dumps({
                                "target": "ACO2",
                                "command": "turn_off",
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                            atuator_states["ACO2"] = False  # Atualiza estado do atuador
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")

                time.sleep(1)

            except Exception as e:
                print(f"Erro no envio de comando: {e}")
                break

    def start_server(self):
        print("Iniciando o Servidor...")
        self.server.bind((self.host, self.port))
        self.server.listen(10)

        print(f"Servidor ouvindo na porta {self.port}")

        if self.ready_event:
            self.ready_event.set()
            print("Servidor está pronto e ouvindo por conexões.")

        # Thread para aceitar conexões
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.start()

        # Thread para regular os dados periodicamente
        control_thread = threading.Thread(target=self.regulate_periodically)
        control_thread.start()
        
    def accept_connections(self):
        while True:
            client_socket, addr = self.server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_handler.start()

# Uso da classe ServerManager3
# Define o ambiente com os métodos get_temperatura, get_umidade e get_co2, e set_limits conforme necessário
# ambiente = ...

# server = ServerManager3(ambiente)
# server.start_server()
