"""
Aplicações Distribuídas - Projeto 2 - coincenter_server.py
Grupo: XX
Números de aluno: 60253
"""

from coincenter_skel import CoinCenterSkeleton
from net_server import NetServer
import select
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_server.py server_ip server_port")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    net_server = NetServer(server_ip, server_port)
    skel = CoinCenterSkeleton()

    sockets = [net_server.server_socket]
    client_sockets = {}  # To track which clients have exited

    print(f"Coin Center Server started on {server_ip}:{server_port}")
    print("Waiting for connections...")

    while True:
        try:
            ready_to_read, _, exceptional = select.select(sockets, [], sockets)
            
            for sock in ready_to_read:
                if sock is net_server.server_socket:
                    # New connection
                    client_sock, client_addr = net_server.accept()
                    sockets.append(client_sock)
                    client_sockets[client_sock] = client_addr
                else:
                    # Existing client sent data
                    request = net_server.recv(sock)
                    
                    if request is None:
                        # Client disconnected
                        print(f"Client {client_sockets.get(sock, 'unknown')} disconnected")
                        sockets.remove(sock)
                        if sock in client_sockets:
                            del client_sockets[sock]
                        sock.close()
                    else:
                        # Process the request
                        print(f"Received request: {request}")
                        response = skel.handle_request(request)
                        print(f"Sending response: {response}")
                        net_server.send(sock, response)
                        
                        # Check if client is exiting
                        if isinstance(request, list) and len(request) >= 2:
                            if request[0] in (40, 90):  # Exit codes
                                print(f"Client {client_sockets.get(sock, 'unknown')} exiting")
                                sockets.remove(sock)
                                if sock in client_sockets:
                                    del client_sockets[sock]
                                sock.close()
            
            # Handle exceptional conditions
            for sock in exceptional:
                print(f"Exceptional condition on socket from {client_sockets.get(sock, 'unknown')}")
                sockets.remove(sock)
                if sock in client_sockets:
                    del client_sockets[sock]
                sock.close()
                
        except KeyboardInterrupt:
            print("\nServer shutting down...")
            break
        except Exception as e:
            print(f"Error in server loop: {e}")
    
    # Close all sockets
    for sock in sockets:
        try:
            sock.close()
        except:
            pass
    
    print("Server closed")

if __name__ == "__main__":
    main()