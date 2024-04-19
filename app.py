from flask import Flask, render_template
from pricebtc import get_price

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '¡Hola Mundo!'

@app.route('/index')
def dasboard():
    value = get_price()
    data={'price':value}
    return render_template('dashboard.html', data = data)

if __name__ == '__main__':
    # Definir el puerto en el que la aplicación va a correr
    port = 5000  # Puedes cambiar este valor al puerto que desees
    app.run(host="0.0.0.0", port=5000,debug=True)
