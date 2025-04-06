"""
Aplicações Distribuídas - Projeto 2 - coincenter_stub.py
Grupo: XX
Números de aluno: 60253
"""
from sock_utils import *
import pickle

class NetServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = create_tcp_server_socket(host, port)

    def accept(self):
        """Accept a new client connection"""
        client_socket, client_address = self.server_socket.accept()
        print(f"New connection from {client_address}")
        return client_socket, client_address

    def recv(self, client_socket):
        """Receive and deserialize data from a client"""
        try:
            # Receive message length
            len_bytes = client_socket.recv(4)
            if not len_bytes:
                return None
                
            msg_len = int.from_bytes(len_bytes, byteorder='big')
            
            # Receive the complete message
            data = receive_all(client_socket, msg_len)
            
            # Deserialize the data
            return pickle.loads(data)
        except ConnectionError:
            print("Client disconnected unexpectedly")
            return None
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None
    
    def send(self, client_socket, data):
        """Serialize and send data to a client"""
        try:
            # Serialize the data
            serialized_data = pickle.dumps(data)
            
            # Send the length of the message followed by the message
            msg_len = len(serialized_data)
            client_socket.sendall(msg_len.to_bytes(4, byteorder='big'))
            client_socket.sendall(serialized_data)
            
            return True
        except Exception as e:
            print(f"Error sending data: {e}")
            return False

    def close(self):
        """Close the server socket"""
        try:
            self.server_socket.close()
            print("Server socket closed")
        except Exception as e:
            print(f"Error closing server socket: {e}")