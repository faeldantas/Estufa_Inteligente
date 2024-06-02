import threading
from Server import ServerManager
from Sensor import *
from Atuador import Atuador
from Ambiente import Ambiente

def start_server(ready_event, ambiente):
    server = ServerManager(ready_event=ready_event, ambiente=ambiente)
    server.start_server()

def start_sensor_temp(ready_event, id, name, ambiente,):
    sensor = Sensor_temp(ready_event=ready_event, id=id, name=name, ambiente=ambiente)
    sensor.run()

def start_sensor_umid(ready_event, id, name, ambiente):
    sensor = Sensor_umid(ready_event=ready_event, id=id, name=name, ambiente=ambiente)
    sensor.run()

def start_sensor_co2(ready_event, id, name, ambiente):
    sensor = Sensor_co2(ready_event=ready_event, id=id, name=name, ambiente=ambiente)
    sensor.run()

def start_actuator(ready_event, id, name, ambiente):
    atuador = Atuador(id=id, name=name, ambiente=ambiente, ready_event=ready_event)
    atuador.run()

#Mudar os valores de ambiente periodicamente
def simulate_environment_changes(ambiente, interval):
    while True:
        ambiente.update_values()
        time.sleep(interval)

if __name__ == "__main__":
    ready_event = threading.Event()
    ambiente = Ambiente(15, 80.0, 0.1, 20, 30, 50, 80, 0.1, 0.9)

    server_thread = threading.Thread(target=start_server, args=(ready_event, ambiente))
    sensor1 = threading.Thread(target=start_sensor_temp, args=(ready_event, "TI001", "Temperatura interna", ambiente))
    # sensor2 = threading.Thread(target=start_sensor_umid, args=(ready_event, "US002","Umidade do solo", ambiente))
    # sensor3 = threading.Thread(target=start_sensor_co2, args=(ready_event, "NCO20","Nivel de CO2", ambiente))
    atuador1 = threading.Thread(target=start_actuator, args=(ready_event, "AA01", "Aquecedor", ambiente))
    # atuador2 = threading.Thread(target=start_actuator, args=(ready_event, "AR02", "Resfriador", ambiente))
    # atuador3 = threading.Thread(target=start_actuator, args=(ready_event, "AI03", "Sisitema de irrigacão", ambiente))
    # atuador4 = threading.Thread(target=start_actuator, args=(ready_event, "ACO2", "Injetor de CO2", ambiente))
    # Iniciar a simulação em uma thread separada
    simulation_thread = threading.Thread(target=simulate_environment_changes, args=(ambiente, 20))

    server_thread.start()
    sensor1.start()
    # sensor2.start()
    # sensor3.start()
    atuador1.start()
    # atuador2.start()
    # atuador3.start()
    # atuador4.start()
    simulation_thread.start()

    server_thread.join()
    sensor1.join()
    # sensor2.join()
    # sensor3.join()
    atuador1.join()
    # atuador2.join()
    # atuador3.join()
    # atuador4.join()
    simulation_thread.join()
