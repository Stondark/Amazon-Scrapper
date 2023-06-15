import random
import os

class Agents:
    
    def __init__(self):
        self.path = "./public/Agents/"
        self.file = self.get_randompath()
        self.user_agent = self.get_useragent(self.file)

    def get_randompath(self):
        return random.choice(os.listdir(self.path))

    def get_useragent(self, file):
        with open(f"{self.path}/{file}") as f:
            agent = f.read().split("\n")
            return random.choice(agent)


agente = Agents()
print(agente.user_agent)