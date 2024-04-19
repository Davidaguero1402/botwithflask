# models/Users.py
import ccxt
class Usuario:
    def __init__(self, apiKey, secretkey):
        self.balance = None
        self.apiKey = apiKey
        self.secretkey = secretkey

    def get_balance(self):
        # Crear una instancia de la clase Binance
        binance = ccxt.binance()

        # Definir el par de divisas para obtener el precio
        symbol = 'BTC/ARS'

        # Obtener el precio actual del par de divisas
        ticker = binance.fetch_ticker(symbol)
        price = ticker['last']
        print(price)
        # Get the amount of BTC in your account

        binance.apiKey = self.apiKey
        binance.secret = self.secretkey
        balance = binance.fetch_balance()
        btc_balance = balance['BTC']['free']

        # Calculate the balance in ARS
        balance_ars = btc_balance * price
        # print(balance_ars)
        return self.balance == balance_ars
