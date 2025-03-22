import socket as s
import sys

def create_tcp_server_socket(address='localhost', port=9999, queue_size=1):
    """
    Cria uma socket de escuta TCP para o servidor.
    
    Parameters:
    address (str): O endereço do servidor (e.g., '127.0.0.1' ou 'localhost').
    port (int): A porta onde o servidor escutará conexões.
    queue_size (int): Número máximo de conexões pendentes na fila.
    
    Returns:
    socket.socket: A socket de escuta do servidor.
    """
    try:
        server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)  # Cria o socket TCP
        server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)  # Allow address reuse
        
        try:
            server_socket.bind((address, port))  # Associa a socket ao endereço e porta
        except PermissionError:
            print(f"Error: No permission to bind to {address}:{port}")
            print("Try running with sudo or use a port > 1024")
            sys.exit(1)
        except s.error as e:
            print(f"Socket error: {e}")
            sys.exit(1)
        
        server_socket.listen(queue_size)  # Começa a escutar por conexões

        print(f"Servidor escutando em {address}:{port} com fila de {queue_size} conexões.")
        
        return server_socket
    except Exception as e:
        print(f"Unexpected error creating server socket: {e}")
        sys.exit(1)

import socket as s
import sys
import traceback

def create_tcp_client_socket(address='localhost', port=9999):
    """
    Creates a TCP client socket to connect to a server with enhanced error reporting.
    
    Parameters:
    address (str): The server address (e.g., '127.0.0.1' or 'localhost').
    port (int): The port where the server is listening.
    
    Returns:
    socket.socket: A client socket connected to the server.
    """
    try:
        # Create the TCP client socket
        client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        
        try:
            # Additional debugging: print connection details
            print(f"Attempting to connect to {address}:{port}")
            
            # Set a timeout for the connection attempt
            client_socket.settimeout(5)  # 5-second timeout
            
            client_socket.connect((address, port))
            
            # Reset timeout after successful connection
            client_socket.settimeout(None)
            
            print(f"Successfully connected to {address}:{port}")
        
        except ConnectionRefusedError:
            print(f"Error: Connection refused to {address}:{port}")
            print("Possible reasons:")
            print("1. Server is not running")
            print("2. Incorrect IP or port")
            print("3. Firewall blocking connection")
            
            # Additional network diagnostics
            try:
                import socket
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                print(f"Local hostname: {hostname}")
                print(f"Local IP: {local_ip}")
            except Exception as diag_error:
                print(f"Could not retrieve network diagnostics: {diag_error}")
            
            sys.exit(1)
        
        except s.timeout:
            print(f"Connection to {address}:{port} timed out")
            print("Possible reasons:")
            print("1. Network connectivity issues")
            print("2. Server not responding")
            sys.exit(1)
        
        except s.error as e:
            print(f"Socket connection error: {e}")
            print("Detailed error traceback:")
            traceback.print_exc()
            sys.exit(1)
        
        return client_socket
    
    except Exception as e:
        print(f"Unexpected error creating client socket: {e}")
        traceback.print_exc()
        sys.exit(1)

def receive_all(socket, length):
    """
    Receives exactly 'length' bytes from the socket.
    
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