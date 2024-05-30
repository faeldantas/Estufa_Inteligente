import threading
from Server import ServerManager
from Sensor import *
from Atuador import Atuador
from Ambiente import Ambiente

def start_server(ready_event, ambiente):
    server = ServerManager(ready_event=ready_event, ambiente=ambiente)
    server.start_server()

def start_sensor_temp(ready_event, name, ambiente,):
    sensor = Sensor_temp(ready_event=ready_event, name=name, ambiente=ambiente)
    sensor.run()

def start_sensor_umid(ready_event, name, ambiente):
    sensor = Sensor_umid(ready_event=ready_event, name=name, ambiente=ambiente)
    sensor.run()

def start_sensor_co2(ready_event, name, ambiente):
    sensor = Sensor_co2(ready_event=ready_event, name=name, ambiente=ambiente)
    sensor.run()

def start_actuator(ready_event, name, ambiente):
    atuador = Atuador(name=name, ambiente=ambiente, ready_event=ready_event)
    atuador.run()

if __name__ == "__main__":
    ready_event = threading.Event()
    ambiente = Ambiente(30, 80.0, 0.1)


    #Mudar os valores de ambiente periodicamente
    def simulate_environment_changes(ambiente, interval):
        while True:
            ambiente.update_values()
            time.sleep(interval)


    



    server_thread = threading.Thread(target=start_server, args=(ready_event, ambiente))
    sensor_thread1 = threading.Thread(target=start_sensor_temp, args=(ready_event, "Sensor de Temperatura", ambiente))
    sensor_thread2 = threading.Thread(target=start_sensor_umid, args=(ready_event, "Sensor de Umidade", ambiente))
    sensor_thread3 = threading.Thread(target=start_sensor_co2, args=(ready_event, "Sensor de CO2", ambiente))
    actuator_thread1 = threading.Thread(target=start_actuator, args=(ready_event, "esguicho", ambiente))
    actuator_thread2 = threading.Thread(target=start_actuator, args=(ready_event, "Painel Solar", ambiente))
    # Iniciar a simulação em uma thread separada
    simulation_thread = threading.Thread(target=simulate_environment_changes, args=(ambiente, 20))

    server_thread.start()
    sensor_thread1.start()
    sensor_thread2.start()
    sensor_thread3.start()
    actuator_thread1.start()
    actuator_thread2.start()
    simulation_thread.start()

    server_thread.join()
    sensor_thread1.join()
    sensor_thread2.join()
    sensor_thread3.join()
    actuator_thread1.join()
    actuator_thread2.join()
    simulation_thread.join()
