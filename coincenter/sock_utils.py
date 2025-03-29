import socket
import sys

def create_tcp_server_socket(address='localhost', port=9999, queue_size=1):
    """
    Create a TCP server socket.
    
    Parameters:
    address (str): The server address (e.g., '127.0.0.1' or 'localhost').
    port (int): The port where the server will listen.
    queue_size (int): Maximum number of queued connections.
    
    Returns:
    socket.socket: The server socket.
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((address, port))
        except PermissionError:
            print(f"Error: No permission to bind to {address}:{port}")
            print("Try running with sudo or use a port > 1024")
            sys.exit(1)
        except socket.error as e:
            print(f"Socket error: {e}")
            sys.exit(1)
        
        server_socket.listen(queue_size)
        print(f"Server listening on {address}:{port}")
        
        return server_socket
    except Exception as e:
        print(f"Unexpected error creating server socket: {e}")
        sys.exit(1)

def create_tcp_client_socket(address='localhost', port=9999):
    """
    Create a TCP client socket.
    
    Parameters:
    address (str): The server address (e.g., '127.0.0.1' or 'localhost').
    port (int): The port where the server is listening.
    
    Returns:
    socket.socket: The client socket.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            print(f"Connecting to {address}:{port}")
            client_socket.connect((address, port))
            print(f"Connected to {address}:{port}")
        except ConnectionRefusedError:
            print(f"Connection refused to {address}:{port}")
            print("Check if the server is running and try again")
            sys.exit(1)
        except socket.error as e:
            print(f"Socket error: {e}")
            sys.exit(1)
        
        return client_socket
    except Exception as e:
        print(f"Unexpected error creating client socket: {e}")
        sys.exit(1)

def receive_all(socket, length):
    """
    Receive exactly 'length' bytes from the socket.
    
    Parameters:
    socket (socket.socket): The socket from which to receive data.
    length (int): The number of bytes to receive.
    
    Returns:
    bytes: The received data.
    """
    data = b''
    remaining = length
    
    while remaining > 0:
        chunk = socket.recv(min(remaining, 4096))
        if not chunk:  # Connection closed
            raise ConnectionError("Connection closed before receiving all data")
        data += chunk
        remaining -= len(chunk)
    
    return data