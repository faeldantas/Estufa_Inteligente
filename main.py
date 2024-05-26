import threading
from Server import ServerManager
from Sensor import Sensor
from Atuador import Atuador

temperatura = 25
umidade = 0.3
co2 = 0.02

def start_server(ready_event):
    server = ServerManager(ready_event=ready_event)
    server.start_server()

def start_sensor(ready_event, sensor_name):
    sensor = Sensor(name=sensor_name, ready_event=ready_event)
    sensor.run()

def start_actuator(ready_event):
    atuador = Atuador(ready_event=ready_event)
    atuador.run()

if __name__ == "__main__":
    # Cria o evento de sincronização
    ready_event = threading.Event()

    # Cria as threads
    server_thread = threading.Thread(target=start_server, args=(ready_event,))
    sensor_thread1 = threading.Thread(target=start_sensor, args=(ready_event, "Sensor de Temperatura"))
    sensor_thread2 = threading.Thread(target=start_sensor, args=(ready_event, "Sensor de Umidade"))
    actuator_thread1 = threading.Thread(target=start_actuator, args=(ready_event,))
    actuator_thread2 = threading.Thread(target=start_actuator, args=(ready_event,))

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
