"""
Aplicações Distribuídas - Projeto 1 - coincenter_data.py
Grupo: XX
Números de aluno: 60253
"""
from typing import Dict, List

class Asset:
    def __init__(self, name:str, symbol:str, price:float, available_supply:int):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.available_supply = available_supply

    def __str__(self):
        return f"Asset: {self.name} ({self.symbol}) - Price: {self.price}, Available: {self.available_supply}"

    def check_availability(self, quantity:int) -> bool:
        return 0 < quantity <= self.available_supply

    def decrease_quntity(self, quantity:int) -> bool:
        if self.check_availability(quantity):
            self.available_supply -= quantity
            return True
        return False

    def increase_quntity(self, quantity):
        self.available_supply += quantity

class User():
    def __init__(self, id):
        self.id = id    
        self.balance = 100
        self.holdings:Dict[str,float] = {}