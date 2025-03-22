"""
Aplicações Distribuídas - Projeto 2 - coincenter_server.py
Grupo: XX
Números de aluno: 60253
"""

import sys
import signal
import socket
import select
import pickle
from sock_utils import *
from coincenter_data import *
from coincenter.coincenter_skel import CoinCenterSkeleton

def initialize_sample_data():
    """Initialize sample assets for testing."""
    AssetController.add_asset("BTC", "Bitcoin", 50000.0, 100)
    AssetController.add_asset("ETH", "Ethereum", 3000.0, 500)
    AssetController.add_asset("ADA", "Cardano", 2.5, 10000)
    AssetController.add_asset("SOL", "Solana", 150.0, 2000)
    AssetController.add_asset("DOT", "Polkadot", 30.0, 5000)
    print("Sample assets initialized")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_server.py server_ip server_port")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    # Initialize sample data
    initialize_sample_data()
    
    # Create server socket
    server_socket = create_tcp_server_socket(server_ip, server_port)
    server_socket.setblocking(False)  # Set non-blocking mode
    
    # Create skeleton
    skeleton = CoinCenterSkeleton()
    
    # Sets for select
    inputs = [server_socket]
    outputs = []
    
    print(f"Coin Center Server started on {server_ip}:{server_port}")
    
    try:
        while inputs:
            # Wait for at least one socket to be ready
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            
            # Handle readable sockets
            for sock in readable:
                if sock is server_socket:
                    # New connection
                    client_socket, client_address = sock.accept()
                    client_socket.setblocking(False)
                    inputs.append(client_socket)
                    print(f"New connection from {client_address}")
                else:
                    # Data from client
                    try:
                        # Receive message length
                        len_bytes = receive_all(sock, 4)
                        if not len_bytes:
                            # Client closed connection
                            print(f"Client closed connection")
                            if sock in inputs:
                                inputs.remove(sock)
                            sock.close()
                            continue
                            
                        msg_len = int.from_bytes(len_bytes, byteorder='big')
                        
                        # Receive message
                        serialized_msg = receive_all(sock, msg_len)
                        
                        # Deserialize message
                        request = pickle.loads(serialized_msg)
                        print(f"Received request: {request}")
                        
                        # Process request
                        response = skeleton.invoke_method(request)
                        print(f"Sending response: {response}")
                        
                        # Serialize response
                        serialized_response = pickle.dumps(response)
                        
                        # Send response length
                        resp_len = len(serialized_response)
                        sock.sendall(resp_len.to_bytes(4, byteorder='big'))
                        
                        # Send response
                        sock.sendall(serialized_response)
                        
                        # Check if client is exiting
                        if request[0] in (40, 90) and response[1]:
                            print(f"Client exiting")
                            if sock in inputs:
                                inputs.remove(sock)
                            sock.close()
                    
                    except ConnectionError:
                        # Client closed connection unexpectedly
                        print(f"Client closed connection unexpectedly")
                        if sock in inputs:
                            inputs.remove(sock)
                        sock.close()
                    
                    except Exception as e:
                        print(f"Error processing request: {e}")
                        if sock in inputs:
                            inputs.remove(sock)
                        sock.close()
            
            # Handle exceptional sockets
            for sock in exceptional:
                print(f"Exceptional condition on socket")
                if sock in inputs:
                    inputs.remove(sock)
                sock.close()
    
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close all sockets
        for sock in inputs:
            sock.close()
        print("Server closed")

if __name__ == "__main__":
    main()