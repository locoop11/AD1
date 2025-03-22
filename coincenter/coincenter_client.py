"""
Aplicações Distribuídas - Projeto 2 - coincenter_client.py
Grupo: XX
Números de aluno: 60253
"""

import sys
import os
from coincenter_stub import CoinCenterStub

def show_manager_menu():
    """Display the menu options for a manager user."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*50)
    print("        COIN CENTER MANAGEMENT INTERFACE")
    print("="*50)
    print("\n[1] List all assets")
    print("[2] Add new asset")
    print("[3] Remove asset")
    print("[4] Exit")
    print("\n" + "="*50)
    
    choice = input("\nEnter your choice (1-4): ")
    return choice

def show_user_menu():
    """Display the menu options for a regular user."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*50)
    print("          COIN CENTER USER INTERFACE")
    print("="*50)
    print("\n[1] List all available assets")
    print("[2] View my portfolio and balance")
    print("[3] Buy asset")
    print("[4] Sell asset")
    print("[5] Exit")
    print("\n" + "="*50)
    
    choice = input("\nEnter your choice (1-5): ")
    return choice

def process_manager_choice(stub, choice):
    """Process the manager's menu choice and send the corresponding request to the server."""
    if choice == '1':
        # List all assets
        response = stub.get_all_assets()
        if response[1]:
            print("\nAvailable Assets:")
            for asset in response[2:]:
                print(asset)
        else:
            print("\nNo assets available.")
        input("\nPress Enter to continue...")
    
    elif choice == '2':
        # Add new asset
        symbol = input("Enter asset symbol: ")
        try:
            price = float(input("Enter asset price: "))
            supply = int(input("Enter available supply: "))
            
            if price <= 0 or supply <= 0:
                print("Error: Price and supply must be positive values.")
                input("\nPress Enter to continue...")
                return True
            
            response = stub.add_asset(symbol, price, supply)
            print("Asset added successfully!" if response[1] else "Failed to add asset.")
        except ValueError:
            print("Invalid input. Price must be a number and supply must be an integer.")
        input("\nPress Enter to continue...")
    
    elif choice == '3':
        # Remove asset
        symbol = input("Enter asset symbol to remove: ")
        response = stub.remove_asset(symbol)
        if response[1]:
            print(f"Asset {response[2]} removed successfully!")
        else:
            print("Failed to remove asset.")
        input("\nPress Enter to continue...")
    
    elif choice == '4':
        # Exit
        response = stub.exit()
        return False
    
    else:
        print("Invalid choice. Please try again.")
        input("\nPress Enter to continue...")
    
    return True

def process_user_choice(stub, choice):
    """Process the user's menu choice and send the corresponding request to the server."""
    if choice == '1':
        # List all available assets
        response = stub.get_all_assets()
        if response[1]:
            print("\nAvailable Assets:")
            for asset in response[2:]:
                print(asset)
        else:
            print("\nNo assets available.")
        input("\nPress Enter to continue...")
    
    elif choice == '2':
        # View my portfolio and balance
        response = stub.get_assets_balance()
        if response[1]:
            print(f"\nYour Balance: ${response[2]:.2f}")
            print("\nYour Portfolio:")
            if len(response) > 3:
                for asset in response[3:]:
                    print(asset)
            else:
                print("Your portfolio is empty.")
        else:
            print("Failed to retrieve portfolio.")
        input("\nPress Enter to continue...")
    
    elif choice == '3':
        # Buy asset
        symbol = input("Enter asset symbol to buy: ")
        try:
            quantity = float(input("Enter quantity to buy: "))
            if quantity <= 0:
                print("Error: Quantity must be positive")
                input("\nPress Enter to continue...")
                return True
                
            response = stub.buy(symbol, quantity)
            print("Purchase successful!" if response[1] else "Purchase failed.")
        except ValueError:
            print("Invalid input. Quantity must be a number.")
        input("\nPress Enter to continue...")
    
    elif choice == '4':
        # Sell asset
        symbol = input("Enter asset symbol to sell: ")
        try:
            quantity = float(input("Enter quantity to sell: "))
            if quantity <= 0:
                print("Error: Quantity must be positive")
                input("\nPress Enter to continue...")
                return True
                
            response = stub.sell(symbol, quantity)
            print("Sale successful!" if response[1] else "Sale failed.")
        except ValueError:
            print("Invalid input. Quantity must be a number.")
        input("\nPress Enter to continue...")
    
    elif choice == '5':
        # Exit
        response = stub.exit()
        return False
    
    else:
        print("Invalid choice. Please try again.")
        input("\nPress Enter to continue...")
    
    return True

def display_welcome(user_id):
    """Display a welcome message."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*50)
    print(f"      WELCOME TO COIN CENTER - USER ID: {user_id}")
    print("="*50)
    print("\nConnecting to server...")

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 coincenter_client.py user_id server_ip server_port")
        sys.exit(1)

    user_id = sys.argv[1]
    server_ip = sys.argv[2]
    server_port = int(sys.argv[3])
    
    # Display welcome message
    display_welcome(user_id)
    
    try:
        # Create client stub
        stub = CoinCenterStub(user_id, server_ip, server_port)
        
        # Check if user is manager (assuming user_id 0 is the manager)
        is_manager = (user_id == "0")
        
        running = True
        while running:
            if is_manager:
                choice = show_manager_menu()
                running = process_manager_choice(stub, choice)
            else:
                choice = show_user_menu()
                running = process_user_choice(stub, choice)
        
        print("\nThank you for using Coin Center. Goodbye!")
        
    except ConnectionRefusedError:
        print(f"\nError: Could not connect to server at {server_ip}:{server_port}")
        print("Please check if the server is running and try again.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    sys.exit(0)

if __name__ == "__main__":
    main()