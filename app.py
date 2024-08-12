from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
from bot import TradingBot
from binance.client import Client
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Inicialmente, o bot não tem pares ou chaves API
bot = None

# Função para obter todos os pares de negociação da Binance
def get_all_pairs(api_key, api_secret):
    try:
        client = Client(api_key, api_secret)
        exchange_info = client.get_exchange_info()
        symbols = [symbol['symbol'] for symbol in exchange_info['symbols']]
        return symbols
    except Exception as e:
        logging.error(f"Erro ao obter pares de moedas: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    global bot
    api_key = request.form.get('api_key')
    api_secret = request.form.get('api_secret')
    pairs = get_all_pairs(api_key, api_secret) if api_key and api_secret else []
    selected_pairs = request.form.getlist('pairs')
    
    if request.method == 'POST' and api_key and api_secret:
        if 'start' in request.form and selected_pairs:
            if not bot or not bot.is_running:
                bot = TradingBot(api_key, api_secret, selected_pairs, '1m', 14, 0.001)
                thread = Thread(target=bot.run)
                thread.start()
                logging.info("Bot iniciado com sucesso.")
        elif 'stop' in request.form and bot:
            bot.stop()
            logging.info("Bot parado com sucesso.")
        return redirect(url_for('index'))

    status = "Rodando" if bot and bot.is_running else "Parado"
    return render_template('index.html', pairs=pairs, selected_pairs=selected_pairs, status=status, api_key=api_key, api_secret=api_secret)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
