"""
Aplicações Distribuídas - Projeto 2 - coincenter_skel.py
Grupo: XX
Números de aluno: 60253
"""

from coincenter_data import Asset, User
from typing import Dict, List

class CoinCenterSkeleton:
    def __init__(self):
        self.assets: List[Asset] = []
        self.users: Dict[int, User] = {0: User(0)}  # Initialize with the manager
        
        # Initialize with some sample assets
        self.assets.append(Asset("Bitcoin", "BTC", 50000.0, 100))
        self.assets.append(Asset("Ethereum", "ETH", 3000.0, 500))
        self.assets.append(Asset("Cardano", "ADA", 2.5, 10000))

    def handle_request(self, request):
        """Process the request from the client and return a response"""
        try:
            if not isinstance(request, list) or len(request) < 2:
                return "Invalid request format"
            
            method_code = request[0]
            user_id = request[-1]
            
            # Ensure user exists
            if user_id not in self.users and user_id != 0:
                self.users[user_id] = User(user_id)
                
            # Route to appropriate handler
            if method_code == 10:
                return self.handle_add_asset(request)
            elif method_code in (20, 50):
                return self.handle_get_all_assets(request)
            elif method_code == 30:
                return self.handle_remove_asset(request)
            elif method_code == 60:
                return self.handle_get_assets_balance(request)
            elif method_code == 70:
                return self.handle_buy(request)
            elif method_code == 80:
                return self.handle_sell(request)
            elif method_code in (40, 90):
                return self.handle_exit(request)
            elif method_code == 100:
                return self.handle_deposit(request)
            elif method_code == 110:
                return self.handle_withdraw(request)
            else:
                return f"Unknown method code: {method_code}"
        except Exception as e:
            return f"Error processing request: {e}"

    def handle_add_asset(self, args):
        """Add a new asset to the system"""
        # [10, asset_name, asset_symbol, asset_price, available_supply, user_id]
        if len(args) < 6 or args[5] != 0:  # Only manager can add assets
            return "Permission denied or invalid arguments"
            
        asset_name = args[1]
        asset_symbol = args[2]
        asset_price = args[3]
        available_supply = args[4]
        
        # Validate inputs
        if not isinstance(asset_price, (int, float)) or not isinstance(available_supply, (int, float)):
            return "Price and supply must be numeric values"
            
        if asset_price <= 0 or available_supply <= 0:
            return "Price and supply must be positive values"
        
        # Check if asset already exists
        if any(asset.symbol == asset_symbol for asset in self.assets):
            return f"Asset with symbol {asset_symbol} already exists"
        
        # Add the asset
        self.assets.append(Asset(asset_name, asset_symbol, asset_price, available_supply))
        return f"Asset {asset_symbol} added successfully"

    def handle_get_all_assets(self, args):
        """Get a list of all assets in the system"""
        if not self.assets:
            return "No assets available"
            
        asset_list = []
        for asset in self.assets:
            asset_list.append(str(asset))
        
        return "\n".join(asset_list)

    def handle_remove_asset(self, args):
        """Remove an asset from the system"""
        # [30, asset_symbol, user_id]
        if len(args) < 3 or args[2] != 0:  # Only manager can remove assets
            return "Permission denied or invalid arguments"
            
        asset_symbol = args[1]
        
        # Find the asset
        asset_to_remove = None
        for asset in self.assets:
            if asset.symbol == asset_symbol:
                asset_to_remove = asset
                break
                
        if not asset_to_remove:
            return f"Asset with symbol {asset_symbol} not found"
        
        # Remove the asset
        self.assets.remove(asset_to_remove)
        return f"Asset {asset_symbol} removed successfully"

    def handle_get_assets_balance(self, args):
        """Get a user's assets and balance"""
        # [60, user_id]
        if len(args) < 2:
            return "Invalid arguments"
            
        user_id = args[1]
        
        if user_id not in self.users:
            return f"User {user_id} not found"
            
        user = self.users[user_id]
        
        # Format the response
        balance_info = f"Your balance: ${user.balance:.2f}"
        
        if not user.holdings:
            return f"{balance_info}\nYour portfolio is empty"
            
        portfolio = []
        for symbol, quantity in user.holdings.items():
            asset = next((a for a in self.assets if a.symbol == symbol), None)
            if asset:
                value = quantity * asset.price
                portfolio.append(f"{symbol}: {quantity} units (${value:.2f})")
        
        return f"{balance_info}\n" + "\n".join(portfolio)

    def handle_buy(self, args):
        """Buy an asset"""
        # [70, asset_symbol_quantity, user_id]
        if len(args) < 3:
            return "Invalid arguments"
            
        asset_symbol_quantity = args[1]
        user_id = args[2]
        
        if user_id not in self.users:
            return f"User {user_id} not found"
            
        # Parse asset symbol and quantity
        try:
            parts = asset_symbol_quantity.split('_')
            if len(parts) != 2:
                return "Invalid buy format. Use: symbol_quantity"
                
            asset_symbol = parts[0]
            quantity = float(parts[1])
            
            # Find the asset
            asset = next((a for a in self.assets if a.symbol == asset_symbol), None)
            if not asset:
                return f"Asset {asset_symbol} not found"
            
            # Check availability
            if not asset.check_availability(quantity):
                return f"Insufficient supply of {asset_symbol}"
                
            # Check user balance
            user = self.users[user_id]
            total_cost = asset.price * quantity
            
            if user.balance < total_cost:
                return f"Insufficient balance. Cost: ${total_cost:.2f}, Your balance: ${user.balance:.2f}"
                
            # Process the purchase
            asset.decrease_quntity(quantity)
            user.balance -= total_cost
            user.holdings[asset_symbol] = user.holdings.get(asset_symbol, 0) + quantity
            
            return f"Successfully purchased {quantity} units of {asset_symbol} for ${total_cost:.2f}"
            
        except Exception as e:
            return f"Error processing buy request: {e}"

    def handle_sell(self, args):
        """Sell an asset"""
        # [80, asset_symbol, quantity, user_id]
        if len(args) < 4:
            return "Invalid arguments"
            
        asset_symbol = args[1]
        quantity = args[2]
        user_id = args[3]
        
        if user_id not in self.users:
            return f"User {user_id} not found"
            
        user = self.users[user_id]
        
        # Check if user owns the asset
        if asset_symbol not in user.holdings:
            return f"You do not own any {asset_symbol}"
            
        # Check if user has enough units
        if user.holdings[asset_symbol] < quantity:
            return f"Insufficient units. You own {user.holdings[asset_symbol]} {asset_symbol}"
            
        # Find the asset
        asset = next((a for a in self.assets if a.symbol == asset_symbol), None)
        if not asset:
            return f"Asset {asset_symbol} not found"
            
        # Process the sale
        total_value = asset.price * quantity
        asset.increase_quntity(quantity)
        user.balance += total_value
        user.holdings[asset_symbol] -= quantity
        
        # Remove from portfolio if quantity is 0
        if user.holdings[asset_symbol] == 0:
            del user.holdings[asset_symbol]
            
        return f"Successfully sold {quantity} units of {asset_symbol} for ${total_value:.2f}"

    def handle_exit(self, args):
        """Handle exit request"""
        # [40, user_id] or [90, user_id]
        return "Goodbye!"

    def handle_deposit(self, args):
        """Handle deposit request"""
        # [100, quantity, user_id]
        if len(args) < 3:
            return "Invalid arguments"
            
        quantity = args[1]
        user_id = args[2]
        
        if not isinstance(quantity, (int, float)) or quantity <= 0:
            return "Deposit amount must be a positive number"
            
        if user_id not in self.users:
            return f"User {user_id} not found"
            
        user = self.users[user_id]
        user.balance += quantity
            
        return f"Successfully deposited ${quantity:.2f}. New balance: ${user.balance:.2f}"

    def handle_withdraw(self, args):
        """Handle withdrawal request"""
        # [110, quantity, user_id]
        if len(args) < 3:
            return "Invalid arguments"
            
        quantity = args[1]
        user_id = args[2]
        
        if not isinstance(quantity, (int, float)) or quantity <= 0:
            return "Withdrawal amount must be a positive number"
            
        if user_id not in self.users:
            return f"User {user_id} not found"
            
        user = self.users[user_id]
        
        if user.balance < quantity:
            return f"Insufficient balance. Your balance: ${user.balance:.2f}"
            
        user.balance -= quantity
            
        return f"Successfully withdrew ${quantity:.2f}. New balance: ${user.balance:.2f}"