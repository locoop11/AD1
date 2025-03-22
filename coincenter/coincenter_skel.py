"""
Aplicações Distribuídas - Projeto 2 - coincenter_skel.py
Grupo: XX
Números de aluno: 60253
"""

import pickle
from coincenter_data import *

class CoinCenterSkeleton:
    def __init__(self):
        """Initialize the skeleton."""
        self.methods = {
            10: self._add_asset,
            20: self._get_all_assets,
            30: self._remove_asset,
            40: self._exit_manager,
            50: self._get_all_assets,
            60: self._get_assets_balance,
            70: self._buy,
            80: self._sell,
            90: self._exit_user
        }
    
    def invoke_method(self, request):
        """
        Invoke the appropriate method based on the request.
        
        Parameters:
        request (list): The request message.
        
        Returns:
        list: The response message.
        """
        try:
            # Validate the request format
            if not isinstance(request, list) or len(request) < 2:
                return [0, False]
            
            # Get the method code
            method_code = request[0]
            
            # Get the user ID
            user_id = request[-1]
            
            # Make sure the user exists
            if user_id not in ClientController.clients:
                if user_id != 0:  # If not manager, create a new user
                    new_user = User(user_id)
                    new_user.deposit(10000.0)  # $10,000 starting balance
                    ClientController.clients[user_id] = new_user
            
            # Invoke the appropriate method
            if method_code in self.methods:
                return self.methods[method_code](request)
            else:
                return [method_code + 1, False]
        
        except Exception as e:
            print(f"Error invoking method: {e}")
            return [0, False]
    
    def _add_asset(self, request):
        """Add a new asset to the system."""
        # [10, asset_symbol, asset_price, available_supply, ID]
        if len(request) < 5:
            return [11, False]
            
        # Validate user is manager
        if request[4] != 0:
            return [11, False]
            
        # Extract parameters
        asset_symbol = request[1]
        asset_price = request[2]
        available_supply = request[3]
        
        # Validate parameters
        if not isinstance(asset_price, (int, float)) or not isinstance(available_supply, (int, float)):
            return [11, False]
            
        if asset_price <= 0 or available_supply <= 0:
            return [11, False]
        
        # Add the asset
        success = AssetController.add_asset(asset_symbol, asset_symbol, asset_price, available_supply)
        return [11, success]
    
    def _get_all_assets(self, request):
        """Get list of all assets in the system."""
        # [20, ID] or [50, ID]
        assets = AssetController.assets
        asset_list = []
        
        for asset in assets:
            asset_list.append(str(asset))
        
        return [request[0] + 1, True] + asset_list if asset_list else [request[0] + 1, False]
    
    def _remove_asset(self, request):
        """Remove an asset from the system."""
        # [30, asset_symbol, ID]
        if len(request) < 3:
            return [31, False]
            
        # Validate user is manager
        if request[2] != 0:
            return [31, False]
            
        # Extract parameters
        asset_symbol = request[1]
        
        # Check if the asset exists
        asset = next((a for a in AssetController.assets if a.symbol == asset_symbol), None)
        if not asset:
            return [31, False]
        
        # Remove the asset
        AssetController.remove_asset(asset_symbol)
        return [31, True, asset_symbol]
    
    def _exit_manager(self, request):
        """Exit the system (manager)."""
        # [40, ID]
        if request[1] != 0:
            return [41, False]
        
        return [41, True]
    
    def _get_assets_balance(self, request):
        """Get the user's assets and balance."""
        # [60, ID]
        user_id = request[1]
        
        # Check if user exists
        if user_id not in ClientController.clients:
            return [61, False]
            
        # Get the user
        user = ClientController.clients[user_id]
        
        # Check if user is a regular user
        if not isinstance(user, User):
            return [61, False]
        
        # Get the user's balance and portfolio
        balance = user.balance
        portfolio = []
        
        for symbol, quantity in user.portfolio.items():
            portfolio.append(f"{symbol}: {quantity}")
        
        return [61, True, balance] + portfolio
    
    def _buy(self, request):
        """Buy an asset."""
        # [70, asset_symbol_quantity, ID]
        if len(request) < 3:
            return [71, False]
            
        # Extract parameters
        asset_symbol_quantity = request[1]
        user_id = request[2]
        
        # Check if user exists
        if user_id not in ClientController.clients:
            return [71, False]
            
        # Get the user
        user = ClientController.clients[user_id]
        
        # Check if user is a regular user
        if not isinstance(user, User):
            return [71, False]
        
        # Parse the asset symbol and quantity
        try:
            parts = asset_symbol_quantity.split('_')
            if len(parts) != 2:
                return [71, False]
                
            asset_symbol = parts[0]
            quantity = float(parts[1])
            
            # Check if the asset exists
            asset = next((a for a in AssetController.assets if a.symbol == asset_symbol), None)
            if not asset:
                return [71, False]
            
            # Check if user has sufficient funds
            if user.balance < asset.price * quantity:
                return [71, False]
            
            # Check if sufficient supply is available
            if asset.available_supply < quantity:
                return [71, False]
            
            # Buy the asset
            success = user.buy_asset(asset_symbol, quantity)
            return [71, success]
        except:
            return [71, False]
    
    def _sell(self, request):
        """Sell an asset."""
        # [80, asset_symbol, quantity, ID]
        if len(request) < 4:
            return [81, False]
            
        # Extract parameters
        asset_symbol = request[1]
        quantity = request[2]
        user_id = request[3]
        
        # Check if user exists
        if user_id not in ClientController.clients:
            return [81, False]
            
        # Get the user
        user = ClientController.clients[user_id]
        
        # Check if user is a regular user
        if not isinstance(user, User):
            return [81, False]
        
        # Check if the user has the asset
        if asset_symbol not in user.portfolio:
            return [81, False]
        
        # Check if the user has enough of the asset
        if user.portfolio[asset_symbol] < quantity:
            return [81, False]
        
        # Sell the asset
        success = user.sell_asset(asset_symbol, quantity)
        return [81, success]
    
    def _exit_user(self, request):
        """Exit the system (user)."""
        # [90, ID]
        return [91, True]