import ccxt
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene las claves de la API desde las variables de entorno
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")

# Utiliza las claves de la API


def get_price():
    # Crea una instancia de la biblioteca ccxt
    exchange = ccxt.binance()

    # Configura las credenciales de API (clave API y clave secreta)
    exchange.apiKey = api_key
    exchange.secret = secret_key
    # Se obtiene el precio de un activo específico
    symbol = 'BTC/USDT'
    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']
    return price
