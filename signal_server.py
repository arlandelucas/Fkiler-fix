from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para armazenar sinais
signals = []

@app.route('/signal', methods=['POST'])
def receive_signal():
    try:
        # Obtém o sinal do corpo da requisição
        signal = request.data.decode('utf-8')
        if not signal:
            return "Sinal vazio não é permitido", 400
        
        # Adiciona o sinal à lista
        signals.append(signal)
        print(f"Sinal recebido: {signal}")
        return "Sinal recebido com sucesso", 200
    except Exception as e:
        # Captura qualquer exceção e retorna um erro
        return f"Erro ao processar o sinal: {str(e)}", 500

@app.route('/get_signals', methods=['GET'])
def get_signals():
    try:
        # Retorna os sinais armazenados em formato JSON
        return jsonify(signals), 200
    except Exception as e:
        # Captura qualquer exceção e retorna um erro
        return f"Erro ao recuperar os sinais: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Executa o servidor na porta 5000 com modo debug ativado
