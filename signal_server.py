from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para armazenar sinais
signals = []

@app.route('/signal', methods=['POST'])
def receive_signal():
    signal = request.data.decode('utf-8')
    signals.append(signal)
    print(f"Sinal recebido: {signal}")
    return "Sinal recebido com sucesso", 200

@app.route('/get_signals', methods=['GET'])
def get_signals():
    return jsonify(signals), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Executa o servidor na porta 5000
