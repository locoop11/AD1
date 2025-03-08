"""
Aplicações Distribuídas - Projeto 1 - net_client.py
Grupo: XX
Números de aluno: 60253
"""
from sock_utils import *

class NetClient:
    def __init__(self, id, host, port):
        """Initialize a network client with the given ID and server information."""
        self.id = id
        self.host = host
        self.port = port
        self.socket = create_tcp_client_socket(host, port)
     
    def send(self, data):
        """Send data to the server, prefixing with the client ID."""
        if data is None:
            data = ""
      
        # Always prepend the client ID to the message
        message = f"{self.id} {data}"
        
        if isinstance(message, str):
            message = message.encode('utf-8')
            
        msg_len = len(message)
        header = msg_len.to_bytes(4, byteorder='big')
        
        self.socket.sendall(header + message)
        
        return True

    def recv(self):
        """Receive and return a response from the server."""
        header = self.socket.recv(4)
        if not header:
            return None
        
        msg_len = int.from_bytes(header, byteorder='big')
        
        chunks = []
        bytes_received = 0
        
        while bytes_received < msg_len:
            chunk = self.socket.recv(min(msg_len - bytes_received, 4096))
            if not chunk:
                break
            chunks.append(chunk)
            bytes_received += len(chunk)
            
        response = b''.join(chunks)
        
        try:
            return response.decode('utf-8')
        except UnicodeDecodeError:
            return response
    
    def close(self):
        """Close the client connection."""
        try:
            self.socket.close()
            print(f"Connection closed for client {self.id}")
        except Exception as e:
            print(f"Error closing connection: {e}")