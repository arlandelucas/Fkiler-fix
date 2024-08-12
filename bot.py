from binance.client import Client
from binance.enums import *
import numpy as np
import time
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TradingBot:
    def __init__(self, api_key, api_secret, pairs, interval, moving_average_period, quantity):
        try:
            self.client = Client(api_key, api_secret)
        except Exception as e:
            logging.error(f"Erro ao conectar com a API da Binance: {e}")
            raise
        
        self.pairs = pairs
        self.interval = interval
        self.moving_average_period = moving_average_period
        self.quantity = quantity
        self.is_running = False

    def get_prices(self, pair):
        try:
            klines = self.client.get_klines(symbol=pair, interval=self.interval, limit=self.moving_average_period)
            prices = [float(entry[4]) for entry in klines]
            return prices
        except Exception as e:
            logging.error(f"Erro ao obter preços para o par {pair}: {e}")
            return []

    def get_moving_average(self, prices):
        return np.mean(prices[-self.moving_average_period:])

    def buy(self, pair):
        try:
            logging.info(f"Comprando {self.quantity} de {pair}")
            order = self.client.order_market_buy(symbol=pair, quantity=self.quantity)
            logging.info(f"Compra realizada: {order}")
        except Exception as e:
            logging.error(f"Erro ao tentar comprar {pair}: {e}")

    def sell(self, pair):
        try:
            logging.info(f"Vendendo {self.quantity} de {pair}")
            order = self.client.order_market_sell(symbol=pair, quantity=self.quantity)
            logging.info(f"Venda realizada: {order}")
        except Exception as e:
            logging.error(f"Erro ao tentar vender {pair}: {e}")

    def run(self):
        self.is_running = True
        try:
            while self.is_running:
                for pair in self.pairs:
                    prices = self.get_prices(pair)
                    if not prices:
                        logging.warning(f"Preços não disponíveis para {pair}. Pulando para o próximo par.")
                        continue
                    current_price = prices[-1]
                    moving_average = self.get_moving_average(prices)
                    logging.info(f"[{pair}] Preço atual: {current_price}, Média Móvel: {moving_average}")
                    if current_price < moving_average:
                        self.buy(pair)
                    elif current_price > moving_average:
                        self.sell(pair)
                time.sleep(60)
        except Exception as e:
            logging.error(f"Erro durante a execução do bot: {e}")
        finally:
            self.is_running = False
            logging.info("Bot parado.")

    def stop(self):
        self.is_running = False
