"""
Aplicações Distribuídas - Projeto 1 - net_server.py
Grupo: XX
Números de aluno: XXXXX XXXXX
"""
from sock_utils import *

class NetServer:
    def __init__(self, host, port):
        """Initialize a network server with the given host and port."""
        self.host = host
        self.port = port
        self.socket = create_tcp_server_socket(host, port)
    
    def accept(self):
        """Accept and return a new client connection."""
        return self.socket.accept()

    def recv(self, client_socket):
        """Receive and return data from a client."""
        # Receive the header with message length (4 bytes)
        header = client_socket.recv(4)
        if not header:
            return None
            
        # Extract message length
        msg_len = int.from_bytes(header, byteorder='big')
        
        # Receive the complete message
        chunks = []
        bytes_received = 0
        
        while bytes_received < msg_len:
            chunk = client_socket.recv(min(msg_len - bytes_received, 4096))
            if not chunk:
                break
            chunks.append(chunk)
            bytes_received += len(chunk)
            
        message = b''.join(chunks)
        
        # Decode the message if it's a string
        try:
            return message.decode('utf-8')
        except UnicodeDecodeError:
            return message
    
    def send(self, client_socket, data):
        """Send data to a client."""
        # Ensure data is not None
        if data is None:
            data = ""
            
        # Convert data to bytes if it's a string
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        # Add data length prefix (4 bytes)
        data_len = len(data)
        header = data_len.to_bytes(4, byteorder='big')
        
        # Send the header followed by the data
        client_socket.sendall(header + data)
        
        return True

    def close(self):
        """Close the server socket."""
        try:
            self.socket.close()
            print("Server socket closed")
        except Exception as e:
            print(f"Error closing server socket: {e}")