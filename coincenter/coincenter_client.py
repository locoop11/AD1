"""
Aplicações Distribuídas - Projeto 1 - coincenter_client.py
Grupo: XX
Números de aluno: XXXXX XXXXX
"""

import sys
import os
from net_client import *

### código do programa principal ###
def show_manager_menu():
    """Display the menu options for a manager user."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*50)
    print("        COIN CENTER MANAGEMENT INTERFACE")
    print("="*50)
    print("\n[1] List all assets")
    print("[2] Add new asset")
    print("[3] Remove asset")
    print("[4] View all users")
    print("[5] View specific user details")
    print("[6] Exit")
    print("\n" + "="*50)
    
    choice = input("\nEnter your choice (1-6): ")
    return choice

def show_user_menu():
    """Display the menu options for a regular user."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*50)
    print("          COIN CENTER USER INTERFACE")
    print("="*50)
    print("\n[1] List all available assets")
    print("[2] View my portfolio")
    print("[3] View my balance")
    print("[4] Buy asset")
    print("[5] Sell asset")
    print("[6] Deposit money")
    print("[7] Withdraw money")
    print("[8] Exit")
    print("\n" + "="*50)
    
    choice = input("\nEnter your choice (1-8): ")
    return choice

def process_manager_choice(client, choice):
    """Process the manager's menu choice and send the corresponding request to the server."""
    if choice == '1':
        # List all assets
        response = client.send("LIST_ASSETS")
        print("\nAvailable Assets:")
        print(client.recv())
        input("\nPress Enter to continue...")
    
    elif choice == '2':
        # Add new asset
        symbol = input("Enter asset symbol: ")
        name = input("Enter asset name: ")
        try:
            price = float(input("Enter asset price: "))
            supply = int(input("Enter available supply: "))
            
            if price <= 0 or supply <= 0:
                print("Error: Price and supply must be positive values.")
                input("\nPress Enter to continue...")
                return True
            
            # Notice the correct format: ADD_ASSET symbol name price supply
            response = client.send(f"ADD_ASSET {symbol} {name} {price} {supply}")
            print(client.recv())
        except ValueError:
            print("Invalid input. Price must be a number and supply must be an integer.")
        input("\nPress Enter to continue...")
    
    elif choice == '3':
        # Remove asset
        symbol = input("Enter asset symbol to remove: ")
        response = client.send(f"REMOVE_ASSET {symbol}")
        print(client.recv())
        input("\nPress Enter to continue...")
    
    elif choice == '4':
        # View all users
        response = client.send("LIST_USERS")
        print("\nRegistered Users:")
        print(client.recv())
        input("\nPress Enter to continue...")
    
    elif choice == '5':
        # View specific user details
        user_id = input("Enter user ID: ")
        try:
            user_id = int(user_id)
            response = client.send(f"USER_DETAILS {user_id}")
            print(f"\nUser {user_id} Details:")
            print(client.recv())
        except ValueError:
            print("Invalid input. User ID must be an integer.")
        input("\nPress Enter to continue...")
    
    elif choice == '6':
        # Exit
        return False
    
    else:
        print("Invalid choice. Please try again.")
        input("\nPress Enter to continue...")
    
    return True

def process_user_choice(client, user_id, choice):
    """Process the user's menu choice and send the corresponding request to the server."""
    if choice == '1':
        # List all available assets
        response = client.send("LIST_ASSETS")
        print("\nAvailable Assets:")
        print(client.recv())
        input("\nPress Enter to continue...")
    
    elif choice == '2':
        # View my portfolio
        response = client.send(f"GET_PORTFOLIO {user_id}")
        print("\nYour Portfolio:")
        print(client.recv())
        input("\nPress Enter to continue...")
    
    elif choice == '3':
        # View my balance
        response = client.send(f"GET_BALANCE {user_id}")
        print("\nYour Balance:")
        print(client.recv())
        input("\nPress Enter to continue...")
    
    elif choice == '4':
        # Buy asset
        symbol = input("Enter asset symbol to buy: ")
        try:
            quantity = float(input("Enter quantity to buy: "))
            response = client.send(f"BUY_ASSET {user_id} {symbol} {quantity}")
            print(client.recv())
        except ValueError:
            print("Invalid input. Quantity must be a number.")
        input("\nPress Enter to continue...")
    
    elif choice == '5':
        # Sell asset
        symbol = input("Enter asset symbol to sell: ")
        try:
            quantity = float(input("Enter quantity to sell: "))
            response = client.send(f"SELL_ASSET {user_id} {symbol} {quantity}")
            print(client.recv())
        except ValueError:
            print("Invalid input. Quantity must be a number.")
        input("\nPress Enter to continue...")
    
    elif choice == '6':
        # Deposit money
        try:
            amount = float(input("Enter amount to deposit: "))
            response = client.send(f"DEPOSIT {user_id} {amount}")
            print(client.recv())
        except ValueError:
            print("Invalid input. Amount must be a number.")
        input("\nPress Enter to continue...")
    
    elif choice == '7':
        # Withdraw money
        try:
            amount = float(input("Enter amount to withdraw: "))
            response = client.send(f"WITHDRAW {user_id} {amount}")
            print(client.recv())
        except ValueError:
            print("Invalid input. Amount must be a number.")
        input("\nPress Enter to continue...")
    
    elif choice == '8':
        # Exit
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
        # Create client connection
        client = NetClient(user_id, server_ip, server_port)
        
        # Check if user is manager (assuming user_id 0 is the manager)
        is_manager = (user_id == "0")
        
        running = True
        while running:
            if is_manager:
                choice = show_manager_menu()
                running = process_manager_choice(client, choice)
            else:
                choice = show_user_menu()
                running = process_user_choice(client, user_id, choice)
        
        # Close the connection when exiting
        print("\nThank you for using Coin Center. Goodbye!")
        client.close()
        
    except ConnectionRefusedError:
        print(f"\nError: Could not connect to server at {server_ip}:{server_port}")
        print("Please check if the server is running and try again.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    sys.exit(0)

if __name__ == "__main__":
    main()