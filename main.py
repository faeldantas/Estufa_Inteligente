import threading
from Server import ServerManager
from Sensor import *
from Atuador import Atuador
from Ambiente import Ambiente




def start_server(ready_event, ambiente):
    server = ServerManager(ready_event=ready_event, ambiente=ambiente)
    server.start_server()

def start_sensor_temp(ready_event, sensor_name, ambiente):
    sensor = Sensor_temp(name=sensor_name, ambiente = ambiente, ready_event=ready_event)
    sensor.run()

def start_sensor_umid(ready_event, sensor_name, ambiente):
    sensor = Sensor_umid(name=sensor_name, ambiente=ambiente, ready_event=ready_event)
    sensor.run()

def start_actuator(ready_event, name, ambiente):
    atuador = Atuador(ready_event=ready_event, name=name, ambiente=ambiente)
    atuador.run()

if __name__ == "__main__":
    # Cria o evento de sincronização
    ready_event = threading.Event()

    ambiente = Ambiente(30, 0.9, 0.1)

    # Cria as threads
    server_thread = threading.Thread(target=start_server, args=(ready_event, ambiente))
    sensor_thread1 = threading.Thread(target=start_sensor_temp, args=(ready_event, "Sensor de Temperatura", ambiente))
    sensor_thread2 = threading.Thread(target=start_sensor_umid, args=(ready_event, "Sensor de Umidade", ambiente))
    actuator_thread1 = threading.Thread(target=start_actuator, args=(ready_event, "esguicho", ambiente))
    actuator_thread2 = threading.Thread(target=start_actuator, args=(ready_event, "Painel solar", ambiente))


    # Inicia as threads
    print("Starting server thread...")
    server_thread.start()
    print("Iniciando Sensor de temperatura...")
    sensor_thread1.start()
    print("Iniciando Sensor de Umidade...")
    sensor_thread2.start()
    print("Starting actuator thread 1...")
    actuator_thread1.start()
    print("Starting actuator thread 2...")
    actuator_thread2.start()

    # Espera que as threads terminem (opcional)
    server_thread.join()
    sensor_thread1.join()
    sensor_thread2.join()
    actuator_thread1.join()
    actuator_thread2.join()
