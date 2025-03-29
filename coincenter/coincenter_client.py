"""
Aplicações Distribuídas - Projeto 2 - coincenter_client.py
Grupo: XX
Números de aluno: 60253
"""

from coincenter_stub import CoinCenterStub
import sys

def is_valid_command(command):
    """Validate if the command has the correct format"""
    if not command:
        return False
    
    parts = command.split(';')
    
    # Check the command type
    cmd_type = parts[0].upper()
    
    # Manager commands
    if cmd_type == "ADD_ASSET" and len(parts) == 5:
        # Validate price and supply are numeric
        try:
            float(parts[3])
            float(parts[4])
            return True
        except ValueError:
            return False
    elif cmd_type == "REMOVE_ASSET" and len(parts) == 2:
        return True
    elif cmd_type == "LIST_ASSETS" and len(parts) == 1:
        return True
    # User commands
    elif cmd_type == "LIST_ASSETS" and len(parts) == 1:
        return True
    elif cmd_type == "BALANCE" and len(parts) == 1:
        return True
    elif cmd_type == "BUY" and len(parts) == 3:
        try:
            float(parts[2])
            return True
        except ValueError:
            return False
    elif cmd_type == "SELL" and len(parts) == 3:
        try:
            float(parts[2])
            return True
        except ValueError:
            return False
    elif cmd_type == "DEPOSIT" and len(parts) == 2:
        try:
            float(parts[1])
            return True
        except ValueError:
            return False
    elif cmd_type == "WITHDRAW" and len(parts) == 2:
        try:
            float(parts[1])
            return True
        except ValueError:
            return False
    
    return False

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 coincenter_client.py user_id server_ip server_port")
        sys.exit(1)

    user_id = int(sys.argv[1])
    server_ip = sys.argv[2]
    server_port = int(sys.argv[3])

    stub = CoinCenterStub(user_id, server_ip, server_port)
    
    print(f"\n{'='*50}")
    print(f"      WELCOME TO COIN CENTER - USER ID: {user_id}")
    print(f"{'='*50}")
    
    if user_id == 0:
        print("\nMANAGER COMMANDS:")
        print("ADD_ASSET;name;symbol;price;supply")
        print("REMOVE_ASSET;symbol")
        print("LIST_ASSETS")
    else:
        print("\nUSER COMMANDS:")
        print("LIST_ASSETS")
        print("BALANCE")
        print("BUY;symbol;quantity")
        print("SELL;symbol;quantity")
        print("DEPOSIT;amount")
        print("WITHDRAW;amount")
    
    print("EXIT (to quit the program)")
    print(f"{'='*50}\n")

    while True:
        command = input("command > ")
        
        if command.upper() == "EXIT":
            stub.exit()
            break
        else:
            if is_valid_command(command):
                response = stub.handle_command(command)
                print(response)
            else:
                print("Invalid command. Please check the format and try again.")

if __name__ == "__main__":
    main()