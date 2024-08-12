from binance.client import Client
from binance.enums import *
import numpy as np
import time

class TradingBot:
    def __init__(self, api_key, api_secret, pairs, interval, moving_average_period, quantity):
        self.client = Client(api_key, api_secret)
        self.pairs = pairs
        self.interval = interval
        self.moving_average_period = moving_average_period
        self.quantity = quantity
        self.is_running = False

    def get_prices(self, pair):
        klines = self.client.get_klines(symbol=pair, interval=self.interval, limit=self.moving_average_period)
        prices = [float(entry[4]) for entry in klines]
        return prices

    def get_moving_average(self, prices):
        return np.mean(prices[-self.moving_average_period:])

    def buy(self, pair):
        print(f"Comprando {self.quantity} de {pair}")
        order = self.client.order_market_buy(symbol=pair, quantity=self.quantity)
        print(f"Compra realizada: {order}")

    def sell(self, pair):
        print(f"Vendendo {self.quantity} de {pair}")
        order = self.client.order_market_sell(symbol=pair, quantity=self.quantity)
        print(f"Venda realizada: {order}")

    def run(self):
        self.is_running = True
        while self.is_running:
            for pair in self.pairs:
                prices = self.get_prices(pair)
                current_price = prices[-1]
                moving_average = self.get_moving_average(prices)
                print(f"[{pair}] Preço atual: {current_price}, Média Móvel: {moving_average}")
                if current_price < moving_average:
                    self.buy(pair)
                elif current_price > moving_average:
                    self.sell(pair)
            time.sleep(60)

    def stop(self):
        self.is_running = False