"""
Aplicações Distribuídas - Projeto 1 - net_client.py
Grupo: XX
Números de aluno: 60253
"""
from sock_utils import *
import pickle

class NetClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = create_tcp_client_socket(self.host, self.port)
     
    def send(self, data):
        """Send data to the server after serializing it"""
        try:
            # Serialize the data using pickle
            serialized_data = pickle.dumps(data)
            
            # Send the length of the message followed by the message
            msg_len = len(serialized_data)
            self.client_socket.sendall(msg_len.to_bytes(4, byteorder='big'))
            self.client_socket.sendall(serialized_data)
            
            return True
        except Exception as e:
            print(f"Error sending data: {e}")
            return False

    def recv(self):
        """Receive and deserialize data from the server"""
        try:
            # Receive the length of the incoming message
            len_bytes = self.client_socket.recv(4)
            if not len_bytes:
                return None
                
            msg_len = int.from_bytes(len_bytes, byteorder='big')
            
            # Receive the complete message
            data = receive_all(self.client_socket, msg_len)
            
            # Deserialize the data
            return pickle.loads(data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None
    
    def close(self):
        """Close the client socket"""
        try:
            self.client_socket.close()
            print("Connection closed")
        except Exception as e:
            print(f"Error closing connection: {e}")