import random


class Ambiente:
    def __init__(self, temp, umid, co2, min_temp, max_temp, min_umid, max_umid, min_co2, max_co2):
        self.temp = temp
        self.umid = umid
        self.co2 = co2
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.min_umid = min_umid
        self.max_umid = max_umid
        self.min_co2 = min_co2
        self.max_co2 = max_co2

    def set_temperatura(self, valor):
        self.temp = valor
        print(f"Temperatura atualizando para: {self.temp}C")
    
    def get_temperatura(self):
        return int(self.temp)
    
    def set_umidade(self, valor):
        self.umid = valor
        print(f"Umidade atualizando para: {self.umid}%")
    
    def get_umidade(self):
        return self.umid
    
    def set_co2(self, valor):
        self.co2 = valor
        print(f"Nível de CO2 atualizando para: {self.co2} ppm")
    
    def get_co2(self):
        return self.co2

    def update_values(self):
        # Simular variação gradual para a temperatura
        temp_change = random.choice([-2, -1, 0, 1, 2])
        self.temp += temp_change
        if self.temp < 0:
            self.temp = 0  # Garantir que a temperatura não fique negativa

        # Simular variação gradual para a umidade
        umid_change = random.uniform(-3.0, 3.0)
        self.umid += umid_change
        if self.umid < 0:
            self.umid = 0  # Garantir que a umidade não fique negativa
        elif self.umid > 100:
            self.umid = 100  # Garantir que a umidade não ultrapasse 100%

        # Simular variação gradual para o nível de CO2
        co2_change = random.uniform(-10, 10)
        self.co2 += co2_change
        if self.co2 < 0:
            self.co2 = 0  # Garantir que o nível de CO2 não fique negativo

        print(f"Valores atualizados: Temperatura={self.temp}C, Umidade={self.umid}%, CO2={self.co2} ppm")
