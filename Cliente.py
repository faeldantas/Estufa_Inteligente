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
        """Tenta conectar ao servidor."""
        if self.ready_event:
            self.ready_event.wait()  # Espera até o servidor estar pronto
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print("Cliente conectado ao servidor.")
        except socket.error as e:
            print(f"Erro ao conectar ao servidor: {e}")
            self.client_socket.close()


    def get_envioronment_limits(self):
        """Obtém os limites do ambiente do usuário."""
        try:
            temp_min = int(input("Digite a temperatura mínima: "))
            temp_max = int(input("Digite a temperatura máxima: "))
            umid_min = int(input("Digite a umidade mínima: "))
            umid_max = int(input("Digite a umidade máxima: "))
            co2_min = int(input("Digite o nível de CO2 mínimo: "))
            co2_max = int(input("Digite o nível de CO2 máximo: "))

            return {
                "action":'define_limits',
                "min_temp": temp_min,
                "max_temp": temp_max,
                "min_umid": umid_min,
                "max_umid": umid_max,
                "min_co2": co2_min,
                "max_co2": co2_max
            }
        except ValueError as e:
            print(f"Entrada inválida: {e}")
            return None


    def send_environment_limits(self):
        """Envia os limites do ambiente ao servidor."""
        environment_limits = self.get_envioronment_limits()
        if environment_limits is None:
            return
        try:
            message = json.dumps(environment_limits) + "\n"
            self.client_socket.sendall(message.encode('utf-8'))  
            print("Limites do ambiente enviados para o servidor.")

        except socket.error as e:
            print(f"Erro ao enviar limites do ambiente: {e}")


    def request_data(self):
        """Solicita o último registro de dados do servidor."""
        try:
            request = json.dumps({"action": "get_latest_data"}) + "\n"
            self.client_socket.sendall(request.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            if response:
                return json.loads(response)
            else:
                print("Nenhum dado recebido do servidor.")
                return None
            
        except socket.error as e:
            print(f"Erro ao solicitar o último registro de dados: {e}")


    def display_data(self, data):
        """Exibe os dados recebidos do servidor conforme a escolha do usuário."""
        if data is None:
            return
        print("\nEscolha uma opção:")
        print("1. Sensor de Temperatura")
        print("2. Sensor de Umidade")
        print("3. Sensor de CO2")
        choice = input("Digite sua escolha: ")
        if choice == '1':
            print(f"Temperatura: {data.get('temperatura', 'N/A')}C°")
        elif choice == '2':
            print(f"Umidade: {data.get('umidade', 'N/A')}%")
        elif choice == '3':
            print(f"CO2: {data.get('co2', 'N/A')} ppm")
        else:
            print("Opção inválida. Tente novamente.")


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
                data = self.request_data()
                self.display_data(data)
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
