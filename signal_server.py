from flask import Flask, request

app = Flask(__name__)

# Rota para receber os sinais de negociação
@app.route('/signal', methods=['POST'])
def receive_signal():
    signal = request.data.decode('utf-8')
    
    # Aqui você pode salvar o sinal em um banco de dados ou arquivo
    # Ou retransmiti-lo para outros terminais
    
    print(f"Sinal recebido: {signal}")
    
    # Retorna uma resposta para o terminal MT4
    return "Sinal recebido com sucesso", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Executa o servidor na porta 5000
