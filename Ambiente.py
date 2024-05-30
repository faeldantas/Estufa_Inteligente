class Ambiente:
    def __init__(self, temp, umid, co2):
        self.temp = temp
        self.umid = umid
        self.co2 = co2

    def set_temperatura(self, valor):
        self.temp = valor
        print(f"Temperatura set to {self.temp}C")
    
    def get_temperatura(self):
        return int(self.temp)
    
    def set_umidade(self, valor):
        self.umid = valor
        print(f"Umidade set to {self.umid}")
    
    def get_umidade(self):
        return self.umid
    
    def set_co2(self, valor):
        self.co2 = valor
        print(f"Nível de CO2 set to {self.co2} ppm")
    
    def get_co2(self):
        return self.co2