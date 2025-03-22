"""
Aplicações Distribuídas - Projeto 2 - coincenter_stub.py
Grupo: XX
Números de aluno: 60253
"""

import pickle
import socket
from sock_utils import receive_all

class CoinCenterStub:
    def __init__(self, user_id, host, port):
        """Initialize the stub with the user ID and server information."""
        self.user_id = int(user_id)
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        
    def add_asset(self, asset_symbol, asset_price, available_supply):
        """Add a new asset to the system."""
        msg = [10, asset_symbol, asset_price, available_supply, self.user_id]
        return self._send_receive(msg)
    
    def get_all_assets(self):
        """Get list of all assets in the system."""
        msg = [20 if self.user_id == 0 else 50, self.user_id]
        return self._send_receive(msg)
    
    def remove_asset(self, asset_symbol):
        """Remove an asset from the system."""
        msg = [30, asset_symbol, self.user_id]
        return self._send_receive(msg)
    
    def get_assets_balance(self):
        """Get the user's assets and balance."""
        msg = [60, self.user_id]
        return self._send_receive(msg)
    
    def buy(self, asset_symbol, quantity):
        """Buy an asset."""
        msg = [70, f"{asset_symbol}_{quantity}", self.user_id]
        return self._send_receive(msg)
    
    def sell(self, asset_symbol, quantity):
        """Sell an asset."""
        msg = [80, asset_symbol, quantity, self.user_id]
        return self._send_receive(msg)
    
    def exit(self):
        """Exit the system."""
        msg = [40 if self.user_id == 0 else 90, self.user_id]
        response = self._send_receive(msg)
        self.close()
        return response
    
    def _send_receive(self, msg):
        """Send a message to the server and return the response."""
        # Serialize the message
        serialized_msg = pickle.dumps(msg)
        
        # Send the length of the message followed by the message
        msg_len = len(serialized_msg)
        self.socket.sendall(msg_len.to_bytes(4, byteorder='big'))
        self.socket.sendall(serialized_msg)
        
        # Receive the response length
        len_bytes = receive_all(self.socket, 4)
        msg_len = int.from_bytes(len_bytes, byteorder='big')
        
        # Receive the response
        serialized_response = receive_all(self.socket, msg_len)
        response = pickle.loads(serialized_response)
        
        return response
    
    def close(self):
        """Close the connection."""
        try:
            self.socket.close()
        except:
            pass