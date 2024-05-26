import multiprocessing
from Server import ServerManager
from Sensor import Sensor
from Atuador import Atuador

def start_server(ready_event):
    server = ServerManager(ready_event=ready_event)
    server.start_server()

def start_sensor(ready_event, sensor_name):
    sensor = Sensor(ready_event=ready_event, name=sensor_name)
    sensor.run()

def start_actuator(ready_event):
    atuador = Atuador(ready_event=ready_event)
    atuador.run()

if __name__ == "__main__":
    # Cria o evento de sincronização
    event = multiprocessing.Event()

    # Cria os processos
    server_process = multiprocessing.Process(target=start_server, args=(event))
    sensor_process1 = multiprocessing.Process(target=start_sensor, args=(event, "Sensor de Temperatura"))
    sensor_process2 = multiprocessing.Process(target=start_sensor, args=(event, "Sensor de umidade"))
    actuator_process1 = multiprocessing.Process(target=start_actuator, args=(event,))
    actuator_process2 = multiprocessing.Process(target=start_actuator, args=(event,))

    # Inicia os processos
    server_process.start()
    sensor_process1.start()
    sensor_process2.start()
    actuator_process1.start()
    actuator_process2.start()

    # Espera que os processos terminem (opcional)
    server_process.join()
    sensor_process1.join()
    sensor_process2.join()
    actuator_process1.join()
    actuator_process2.join()
