"""
Aplicações Distribuídas - Projeto 1 - coincenter_server.py
Grupo: XX
Números de aluno: 60253
"""

import sys
import signal
import threading
from net_server import *
from coincenter_data import *


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
                
            print(f"Received request: '{request}' from {client_address}")
            
            # Process request and get response
            response = process_request(request)
            
            # Debug
            print(f"Sending response: '{response}' to {client_address}")
            
            # Send response back to client
            server.send(client_socket, response)
            
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
        import traceback
        traceback.print_exc()  # Print the full exception traceback
    finally:
        print(f"Connection from {client_address} closed")

def process_request(request):
    """Process a client request and return the appropriate response."""
    # Split the request into command and parameters
    parts = request.strip().split()
    
    if not parts:
        return "ERROR: Empty request"
    
    # The first part is the user ID, the second part is the command
    if len(parts) < 2:
        return "ERROR: Malformed request"
        
    user_id = parts[0]  # The user ID of the sender
    command = parts[1]  # The actual command
    
    # Ensure the user exists in the system
    if user_id.isdigit():
        sender_id = int(user_id)
        if sender_id not in ClientController.clients:
            if sender_id != 0:  # If not manager, create a new user
                new_user = User(sender_id)
                new_user.deposit(10000.0)  # $10,000 starting balance
                ClientController.clients[sender_id] = new_user
    else:
        return "ERROR: Invalid user ID"
    
    # Handle commands
    if command == "LIST_ASSETS":
        return AssetController.list_all_assets()
    
    elif command == "BUY_ASSET" and len(parts) >= 4:
        try:
            symbol = parts[2] 
            quantity = float(parts[3])
            
            client = ClientController.clients.get(sender_id)
            if client and isinstance(client, User):
                # Check if the asset exists
                asset = next((a for a in AssetController.assets if a.symbol == symbol), None)
                if not asset:
                    return f"ERROR: Asset {symbol} does not exist"
                
                # Check if user has sufficient funds
                if client.balance < asset.price * quantity:
                    return f"ERROR: Insufficient funds. You need ${asset.price * quantity:.2f} but your balance is ${client.balance:.2f}"
                
                # Check if sufficient supply is available
                if asset.available_supply < quantity:
                    return f"ERROR: Insufficient supply. Only {asset.available_supply} units available of {symbol}"
                
                success = client.buy_asset(symbol, quantity)
                if success:
                    return f"Successfully purchased {quantity} units of {symbol}"
                return "ERROR: Transaction failed"
            return f"ERROR: User {sender_id} not found or is not a regular user"
        except ValueError as e:
            print(f"DEBUG: ValueError in BUY_ASSET: {e}")
            return "ERROR: Invalid quantity format. Must be a number."
    
    elif command == "SELL_ASSET" and len(parts) >= 4:
        try:
            symbol = parts[2]
            quantity = float(parts[3])
            
            client = ClientController.clients.get(sender_id)
            if client and isinstance(client, User):
                # Check if user has enough of the asset to sell
                if client.portfolio.get(symbol, 0) < quantity:
                    return f"ERROR: Insufficient assets. You only have {client.portfolio.get(symbol, 0)} units of {symbol}"
                
                success = client.sell_asset(symbol, quantity)
                if success:
                    return f"Successfully sold {quantity} units of {symbol}"
                return "ERROR: Transaction failed"
            return f"ERROR: User {sender_id} not found or is not a regular user"
        except ValueError:
            return "ERROR: Invalid quantity"
    
    elif command == "GET_PORTFOLIO":
        client = ClientController.clients.get(sender_id)
        if client and isinstance(client, User):
            if not client.portfolio:
                return "Your portfolio is empty"
            
            portfolio_details = []
            total_value = 0.0
            
            for symbol, quantity in client.portfolio.items():
                asset = next((a for a in AssetController.assets if a.symbol == symbol), None)
                if asset:
                    value = asset.price * quantity
                    total_value += value
                    portfolio_details.append(f"{symbol}: {quantity} units (${value:.2f})")
            
            return "\n".join(portfolio_details) + f"\n\nTotal Portfolio Value: ${total_value:.2f}"
        return f"ERROR: User {sender_id} not found or is not a regular user"
    
    elif command == "GET_BALANCE":
        client = ClientController.clients.get(sender_id)
        if client and isinstance(client, User):
            return f"Your balance: ${client.balance:.2f}"
        return f"ERROR: User {sender_id} not found or is not a regular user"
    
    elif command == "DEPOSIT" and len(parts) >= 3:
        try:
            # Make sure we're reading the correct parameter
            amount = float(parts[2])
            
            # Debug print to verify the amount
            print(f"DEBUG: Deposit request - User ID: {sender_id}, Amount: {amount}")
            
            client = ClientController.clients.get(sender_id)
            if client and isinstance(client, User):
                if amount <= 0:
                    return "ERROR: Deposit amount must be positive"
                
                client.deposit(amount)
                return f"Successfully deposited ${amount:.2f}. New balance: ${client.balance:.2f}"
            return f"ERROR: User {sender_id} not found or is not a regular user"
        except ValueError as e:
            print(f"DEBUG: ValueError in DEPOSIT: {e}")
            return "ERROR: Invalid amount"
    
    elif command == "WITHDRAW" and len(parts) >= 3:
        try:
            # Make sure we're reading the correct parameter
            amount = float(parts[2])
            
            # Debug print to verify the amount
            print(f"DEBUG: Withdraw request - User ID: {sender_id}, Amount: {amount}")
            
            client = ClientController.clients.get(sender_id)
            if client and isinstance(client, User):
                if amount <= 0:
                    return "ERROR: Withdrawal amount must be positive"
                
                if amount > client.balance:
                    return f"ERROR: Insufficient funds. Your balance is ${client.balance:.2f}"
                
                client.withdraw(amount)
                return f"Successfully withdrew ${amount:.2f}. New balance: ${client.balance:.2f}"
            return f"ERROR: User {sender_id} not found or is not a regular user"
        except ValueError as e:
            # Add more detailed error logging
            print(f"DEBUG: ValueError in WITHDRAW: {e}")
            return "ERROR: Invalid amount"
            
    elif command == "USER_DETAILS":
        # Only manager can see user details
        requester = ClientController.clients.get(sender_id)
        if sender_id != 0:  # Manager ID is 0
            return "ERROR: Only manager can view user details"
        
        if len(parts) < 3:
            return "ERROR: Missing user ID parameter"
            
        try:
            target_id = int(parts[2])
            target_user = ClientController.clients.get(target_id)
            
            if not target_user:
                return f"ERROR: User {target_id} not found"
            
            if not isinstance(target_user, User):
                return f"User {target_id} is a manager, not a regular user"
            
            # Get portfolio value
            portfolio_value = 0.0
            portfolio_details = []
            
            for symbol, quantity in target_user.portfolio.items():
                asset = next((a for a in AssetController.assets if a.symbol == symbol), None)
                if asset:
                    value = asset.price * quantity
                    portfolio_value += value
                    portfolio_details.append(f"{symbol}: {quantity} units (${value:.2f})")
            
            return f"User ID: {target_id}\nBalance: ${target_user.balance:.2f}\nPortfolio Value: ${portfolio_value:.2f}\n" + (
                "\nPortfolio:\n" + "\n".join(portfolio_details) if portfolio_details else "\nPortfolio: Empty"
            )
        except ValueError:
            return "ERROR: Invalid user ID format"
    
    elif command == "ADD_ASSET" and len(parts) >= 5:
        # Ensure sender is manager
        if sender_id != 0:  # Manager ID is 0
            return "ERROR: Only manager can add assets"
        
        try:
            symbol = parts[2]
            name = parts[3]
            price = float(parts[4])
            supply = int(parts[5])
            
            if price <= 0 or supply <= 0:
                return "ERROR: Price and supply must be positive"
            
            success = AssetController.add_asset(symbol, name, price, supply)
            if success:
                return f"Successfully added asset {name} ({symbol})"
            return f"ERROR: Asset with symbol {symbol} already exists"
        except ValueError:
            return "ERROR: Invalid price or supply format"
        except IndexError:
            return "ERROR: Missing parameters for ADD_ASSET command"
    
    elif command == "REMOVE_ASSET" and len(parts) >= 3:
        # Ensure sender is manager
        if sender_id != 0:  # Manager ID is 0
            return "ERROR: Only manager can remove assets"
        
        symbol = parts[2]
        
        # Check if the asset exists
        asset = next((a for a in AssetController.assets if a.symbol == symbol), None)
        if not asset:
            return f"ERROR: Asset {symbol} does not exist"
        
        AssetController.remove_asset(symbol)
        return f"Successfully removed asset {symbol}"
    
    elif command == "LIST_USERS":
        # Ensure sender is manager
        if sender_id != 0:  # Manager ID is 0
            return "ERROR: Only manager can list users"
        
        users = [client for client_id, client in ClientController.clients.items() if isinstance(client, User)]
        
        if not users:
            return "No users registered"
        
        user_info = []
        for user in users:
            # Calculate portfolio value
            portfolio_value = 0.0
            for symbol, quantity in user.portfolio.items():
                asset = next((a for a in AssetController.assets if a.symbol == symbol), None)
                if asset:
                    portfolio_value += asset.price * quantity
            
            user_info.append(f"User ID: {user.id} - Balance: ${user.balance:.2f} - Portfolio Value: ${portfolio_value:.2f}")
        
        return "\n".join(user_info)
        
    # Default response if no conditions match
    return f"ERROR: Unknown or malformed command: {command}"

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