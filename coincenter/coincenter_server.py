"""
Aplicações Distribuídas - Projeto 1 - coincenter_server.py
Grupo: XX
Números de aluno: XXXXX XXXXX
"""

import sys
import signal
import threading
from net_server import *
from coincenter_data import *

### código do programa principal ###
server = None

def handle_shutdown(signum, frame):
    """Handle server shutdown when SIGINT is received."""
    global server
    print("\nShutting down server...")
    server.close()
    sys.exit(0)

def handle_client(client_socket, client_address):
    """Handle communication with a connected client."""
    print(f"New connection from {client_address}")
    
    try:
        while True:
            # Receive request from client
            request = server.recv(client_socket)
            
            if not request:  # Client disconnected
                break
                
            print(f"Received request: {request} from {client_address}")
            
            # Process request and get response
            response = process_request(request)
            
            # Send response back to client
            server.send(client_socket, response)
            
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        print(f"Connection from {client_address} closed")

def process_request(request):
    """Process a client request and return the appropriate response."""
    # Split the request into command and parameters
    parts = request.strip().split()
    
    if not parts:
        return "ERROR: Empty request"
    
    # Extract the user ID (first part) and the actual command (second part)
    user_id = parts[0]
    
    if len(parts) < 2:
        return "ERROR: Malformed request"
        
    command = parts[1]
    
    # Manager commands
    if command == "LIST_ASSETS":
        return AssetController.list_all_assets()
        
    elif command == "ADD_ASSET" and len(parts) >= 6:  # Changed from 5 to 6 to account for user_id
        symbol = parts[2]  # Changed from parts[1] to parts[2]
        name = parts[3]    # Changed from parts[2] to parts[3]
        try:
            price = float(parts[4])    # Changed from parts[3] to parts[4]
            supply = int(parts[5])     # Changed from parts[4] to parts[5]
            success = AssetController.add_asset(symbol, name, price, supply)
            return "Asset added successfully" if success else "ERROR: Asset with this symbol already exists"
        except ValueError:
            return "ERROR: Invalid price or supply values"
            
    elif command == "REMOVE_ASSET" and len(parts) >= 3:  # Changed from 2 to 3
        symbol = parts[2]  # Changed from parts[1] to parts[2]
        AssetController.remove_asset(symbol)
        return f"Asset {symbol} removed (if it existed)"
        
    elif command == "LIST_USERS":
        user_list = []
        for user_id, client in ClientController.clients.items():
            if isinstance(client, User):
                user_list.append(f"User ID: {user_id}")
        return "No users registered" if not user_list else "\n".join(user_list)
        
    elif command == "USER_DETAILS" and len(parts) >= 3:  # Changed from 2 to 3
        try:
            requested_user_id = int(parts[2])  # Changed from parts[1] to parts[2]
            client = ClientController.clients.get(requested_user_id)
            if client and isinstance(client, User):
                return str(client)
            return f"ERROR: User {requested_user_id} not found"
        except ValueError:
            return "ERROR: Invalid user ID"
    
    # User commands - update all indices in similar fashion
    elif command == "GET_PORTFOLIO" and len(parts) >= 3:
        try:
            requested_user_id = int(parts[2])
            client = ClientController.clients.get(requested_user_id)
            if client and isinstance(client, User):
                if not client.portfolio:
                    return "Your portfolio is empty"
                
                portfolio_info = []
                for symbol, quantity in client.portfolio.items():
                    asset = next((a for a in AssetController.assets if a.symbol == symbol), None)
                    if asset:
                        value = quantity * asset.price
                        portfolio_info.append(f"{symbol}: {quantity} units (${value:.2f})")
                
                return "\n".join(portfolio_info)
            return f"ERROR: User {requested_user_id} not found"
        except ValueError:
            return "ERROR: Invalid user ID"
            
    # Continue with the same pattern for all other commands...
    # Adjusting all the part indices by +1 to account for the user_id prefix
            
    else:
        return "ERROR: Unknown or malformed command"

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
    
    global server

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, handle_shutdown)
    
    # Initialize sample data
    initialize_sample_data()
    
    # Create server
    server = NetServer(server_ip, server_port)
    print(f"Coin Center Server started on {server_ip}:{server_port}")
    
    # Main server loop
    while True:
        try:
            # Accept new client connection
            client_socket, client_address = server.accept()
            
            # Start a new thread to handle this client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_thread.daemon = True  # Thread will close when main program exits
            client_thread.start()
            
        except Exception as e:
            print(f"Error accepting connection: {e}")

if __name__ == "__main__":
    main()