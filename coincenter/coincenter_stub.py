"""
Aplicações Distribuídas - Projeto 2 - coincenter_stub.py
Grupo: XX
Números de aluno: 60253
"""

from net_client import NetClient
import pickle

class CoinCenterStub:
    def __init__(self, user_id, server_ip, server_port):
        self.id = user_id
        self.net_client = NetClient(server_ip, server_port)

    def handle_command(self, command):
        response = None
        command_parts = command.split(";")
        command_type = command_parts[0].upper()
        
        if self.id == 0:  # manager's commands
            if command_type == "ADD_ASSET":
                response = self.add_asset(command_parts[1], command_parts[2], 
                                         float(command_parts[3]), float(command_parts[4]))
            elif command_type == "REMOVE_ASSET":
                response = self.remove_asset(command_parts[1])
            elif command_type == "LIST_ASSETS":
                response = self.get_all_assets()
        else:  # user's commands
            if command_type == "LIST_ASSETS":
                response = self.get_all_assets()
            elif command_type == "BALANCE":
                response = self.get_assets_balance()
            elif command_type == "BUY":
                response = self.buy(f"{command_parts[1]}_{command_parts[2]}")
            elif command_type == "SELL":
                response = self.sell(command_parts[1], float(command_parts[2]))
            elif command_type == "DEPOSIT":
                response = self.deposit(float(command_parts[1]))
            elif command_type == "WITHDRAW":
                response = self.withdraw(float(command_parts[1]))

        return response
            
    def add_asset(self, asset_name, asset_symbol, asset_price, available_supply):
        request = [10, asset_name, asset_symbol, asset_price, available_supply, self.id]
        self.net_client.send(request)
        response = self.net_client.recv()
        return response

    def get_all_assets(self):
        request = [20 if self.id == 0 else 50, self.id]
        self.net_client.send(request)
        return self.net_client.recv()

    def remove_asset(self, asset_symbol):
        request = [30, asset_symbol, self.id]
        self.net_client.send(request)
        return self.net_client.recv()

    def get_assets_balance(self):
        request = [60, self.id]
        self.net_client.send(request)
        return self.net_client.recv()

    def buy(self, asset_symbol_quantity):
        request = [70, asset_symbol_quantity, self.id]
        self.net_client.send(request)
        return self.net_client.recv()

    def sell(self, asset_symbol, quantity):
        request = [80, asset_symbol, quantity, self.id]
        self.net_client.send(request)
        return self.net_client.recv()

    def deposit(self, quantity):
        request = [100, quantity, self.id]
        self.net_client.send(request)
        return self.net_client.recv()

    def withdraw(self, quantity):
        request = [110, quantity, self.id]
        self.net_client.send(request)
        return self.net_client.recv()

    def exit(self):
        request = [40 if self.id == 0 else 90, self.id]
        self.net_client.send(request)
        response = self.net_client.recv()
        self.net_client.close()
        return response