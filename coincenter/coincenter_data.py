"""
Aplicações Distribuídas - Projeto 1 - coincenter_data.py
Grupo: XX
Números de aluno: 60253
"""
from typing import Dict,List
from abc import ABC, abstractmethod

class Asset:
    def __init__(self, symbol:str, name:str, price:float, available_supply:int):
        self.symbol = symbol
        self.name = name
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


class AssetController:
    assets: List[Asset] = []

    @staticmethod
    def list_all_assets() -> str:
        return "No assets available." if not AssetController.assets else "\n".join(map(str, AssetController.assets))

    @staticmethod
    def remove_asset(symbol: str):
        AssetController.assets = [asset for asset in AssetController.assets if asset.symbol != symbol]

    @staticmethod
    def add_asset(symbol: str, name: str, price: float, available_supply: int):
        if any(asset.symbol == symbol for asset in AssetController.assets):
            return False
        AssetController.assets.append(Asset(symbol, name, price, available_supply))
        return True

class Client(ABC):
    def __init__(self, id):
        self.id = id
    
    @abstractmethod
    def process_request(self, _):
        pass

class User(Client):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.balance = 0.0
        self.portfolio = {}

    def __str__(self):
        return f"User {self.id} - Balance: {self.balance}, Portfolio: {self.portfolio}"

    def buy_asset(self, asset_symbol: str, quantity: float) -> bool:
        # Debug print
        print(f"DEBUG: User.buy_asset - Symbol: {asset_symbol}, Quantity: {quantity}")
        
        asset = next((a for a in AssetController.assets if a.symbol == asset_symbol), None)
        if asset and asset.available_supply >= quantity and self.balance >= asset.price * quantity:
            asset.available_supply -= quantity
            self.balance -= asset.price * quantity
            self.portfolio[asset_symbol] = self.portfolio.get(asset_symbol, 0) + quantity
            return True
        return False
    
    def sell_asset(self, asset_symbol: str, quantity: float) -> bool:
        if self.portfolio.get(asset_symbol, 0) >= quantity:
            asset = next((a for a in AssetController.assets if a.symbol == asset_symbol), None)
            if asset:
                asset.available_supply += quantity
                self.balance += asset.price * quantity
                self.portfolio[asset_symbol] -= quantity
                if self.portfolio[asset_symbol] == 0:
                    del self.portfolio[asset_symbol]
                return True
        return False

    def deposit(self, amount: float):
        if amount > 0:
            self.balance += amount

    def withdraw(self, amount: float):
        if 0 < amount <= self.balance:
            self.balance -= amount

    def process_request(self, request) -> str:
        return f"Processing request {request} for user {self.id}"

class Manager(Client):
    def __init__(self, user_id):
        super().__init__(user_id)

    def process_request(self, request):
        return f"Manager {self.id} processing request: {request}"

class ClientController:
    clients: Dict[int, Client] = {0: Manager(0)}

    @staticmethod
    def process_request(request: str) -> str:
        client_id = int(request.split()[0])  # Supondo que o ID do cliente seja a primeira parte do request
        
        if client_id not in ClientController.clients:
            ClientController.clients[client_id] = User(client_id)
        
        return ClientController.clients[client_id].process_request(request)
