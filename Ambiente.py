import random

#Classe criada para simular monitoramento e mudanças de ambiente
class Ambiente:
    def __init__(self, temp, umid, co2, min_temp=None, max_temp=None, min_umid=None, max_umid=None, min_co2=None, max_co2=None):
        self.temp = temp
        self.umid = umid
        self.co2 = co2

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
        print(f"Nivel de CO2 atualizando para: {self.co2} ppm")
    
    def get_co2(self):
        return self.co2

    #Modifica valores gradualmente(Tenta simular comportamento natural)
    def update_values(self):
        # Simular variação gradual para a temperatura
        temp_noise = random.choice([-2, -1, 0, 1, 2])
        self.change_temp(temp_noise)

        # Simular variação gradual para a umidade
        umid_noise = random.uniform(-3.0, 3.0)
        self.umid_change(umid_noise)

        # Simular variação gradual para o nível de CO2
        co2_noise = random.uniform(-100, 30)
        self.co2_change(co2_noise)

        print(f"Valores atualizados: Temperatura={self.temp}C, Umidade={self.umid}%, CO2={self.co2} ppm")
    

    def change_temp(self, noise):
        self.temp += noise
        if self.temp < 0:
            self.temp = 0  


    def umid_change(self, noise):
        self.umid += noise
        if self.umid < 0:
            self.umid = 0  
        elif self.umid > 100:
            self.umid = 100  


    def co2_change(self, noise):
        self.co2 += noise
        if self.co2 < 0:
            self.co2 = 0  
    
    def set_limits(self, min_temp, max_temp, min_umid, max_umid, min_co2, max_co2):
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.min_umid = min_umid
        self.max_umid = max_umid
        self.min_co2 = min_co2
        self.max_co2 = max_co2