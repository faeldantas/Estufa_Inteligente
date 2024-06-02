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


    def regulate_periodically(self):
        while True:
            try:
                #verifica Resfriador
                if self.ambiente.get_temperatura() > self.ambiente.max_temp:
                    print(f"Temperatura acima de {self.ambiente.max_temp}, enviando comando para reduzir temperatura.")
                    for client in self.client_sockets:
                        try:
                            #print("Enviando comando para um cliente." + '\n')
                            command = json.dumps({
                                "target": "AR02",
                                "command": "turn_on",
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")
                else:
                    for client in self.client_sockets:
                        try:
                            #print("Enviando comando para um cliente." + '\n')
                            command = json.dumps({
                                "target": "AR02",
                                "command": "turn_off",
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")
                time.sleep(1)  # Esperar 5 segundos antes de enviar o próximo comando

                #varifica aquecedor
                if self.ambiente.get_temperatura() < self.ambiente.min_temp:
                    print(f"Temperatura a baixo de {self.ambiente.max_temp}, enviando comando para aumenta-la.")
                    for client in self.client_sockets:
                        try:
                            #print("Enviando comando para um cliente." + '\n')
                            command = json.dumps({
                                "target": "AA01",
                                "command": "turn_on",
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")
                else:
                    for client in self.client_sockets:
                        try:
                            #print("Enviando comando para um cliente." + '\n')
                            print("tentando desligar")
                            command = json.dumps({
                                "target": "AA01",
                                "command": "turn_off",
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")
                time.sleep(1)  # Esperar 5 segundos antes de enviar o próximo comando


                #verifica umidade
                if self.ambiente.get_umidade() < self.ambiente.min_umid:
                    print(f"Umidade a baixo de {self.ambiente.min_umid}%, enviando comando para aumenta-la.")
                    for client in self.client_sockets:
                        try:
                            #print("Enviando comando para um cliente." + '\n')
                            command = json.dumps({
                                "target": "AI03",
                                "command": "turn_on",
                                "value": self.ambiente.get_co2() + 1,
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")
                else:
                    for client in self.client_sockets:
                        try:
                            #print("Enviando comando para um cliente." + '\n')
                            command = json.dumps({
                                "target": "AI03",
                                "command": "turn_off",
                                "value": self.ambiente.get_co2() + 1,
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")

                time.sleep(1) 

                #Verifica CO2
                if self.ambiente.get_co2() < self.ambiente.min_co2:
                    print("Nivvel de CO2 baixo, enviando comando para aumenta-lo.")
                    for client in self.client_sockets:
                        try:
                            #print("Enviando comando para um cliente." + '\n')
                            command = json.dumps({
                                "target": "ACO2",
                                "command": "turn_on",
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")
                else:
                    for client in self.client_sockets:
                        try:
                            #print("Enviando comando para um cliente." + '\n')
                            command = json.dumps({
                                "target": "ACO2",
                                "command": "turn_on",
                            }) + "\n"
                            client.send(command.encode('utf-8'))
                        except Exception as client_error:
                            print(f"Erro ao enviar comando para um cliente: {client_error}")
                time.sleep(1)  # Esperar 5 segundos antes de enviar o próximo comando

                
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
            control_thread = threading.Thread(target=self.regulate_periodically)
            control_thread.start()

            while True:
                client_socket, addr = self.server.accept()
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_handler.start()
                

        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server.close()