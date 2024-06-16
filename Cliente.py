import socket
import json
import threading

class Cliente:
    def __init__(self, server_host='127.0.0.1', server_port=9999, ready_event=None):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ready_event = ready_event

    def connect(self):
        if self.ready_event:
            self.ready_event.wait()  # Espera até o servidor estar pronto
        self.client_socket.connect((self.server_host, self.server_port))
        print("Cliente conectado ao servidor.")

    def send_environment_limits(self):
        try:
            temp_min = int(input("Digite a temperatura mínima: "))
            temp_max = int(input("Digite a temperatura máxima: "))
            umid_min = int(input("Digite a umidade mínima: "))
            umid_max = int(input("Digite a umidade máxima: "))
            co2_min = int(input("Digite o nível de CO2 mínimo: "))
            co2_max = int(input("Digite o nível de CO2 máximo: "))

            environment_limits = {
                "action":'define_limits',
                "min_temp": temp_min,
                "max_temp": temp_max,
                "min_umid": umid_min,
                "max_umid": umid_max,
                "min_co2": co2_min,
                "max_co2": co2_max
            }
            message = json.dumps(environment_limits) + "\n"
            self.client_socket.sendall(message.encode('utf-8'))  # Use sendall para garantir que todos os dados sejam enviados
            print("Limites do ambiente enviados para o servidor.")
        except Exception as e:
            print(f"Erro ao enviar limites do ambiente: {e}")

    def request_latest_data(self):
        try:
            request = json.dumps({"action": "get_latest_data"}) + "\n"
            self.client_socket.sendall(request.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            if response:
                data = json.loads(response)
                print(f"Último registro de dados: {data}")
            else:
                print("Nenhum dado recebido do servidor.")
        except Exception as e:
            print(f"Erro ao solicitar o último registro de dados: {e}")

    def receive_server_commands(self):
        while True:
            try:
                response = self.client_socket.recv(1024).decode('utf-8')
                if response:
                    print(f"Comando recebido do servidor: {response}")
                else:
                    break  # Se não há dados, a conexão foi fechada
            except Exception as e:
                print(f"Erro ao receber comando do servidor: {e}")
                break

    def run(self):
        self.connect()
        # threading.Thread(target=self.receive_server_commands).start()
        while True:
            print("\nEscolha uma opção:")
            print("1. Enviar limites de ambiente")
            print("2. Solicitar último registro de dados")
            print("3. Sair")
            choice = input("Digite sua escolha: ")
            if choice == '1':
                self.send_environment_limits()
            elif choice == '2':
                self.request_latest_data()
            elif choice == '3':
                print("Encerrando o cliente.")
                self.client_socket.close()
                break
            else:
                print("Opção inválida. Tente novamente.")

# Exemplo de uso:
ready_event = threading.Event()
cliente = Cliente(ready_event=ready_event)
ready_event.set()
cliente.run()
