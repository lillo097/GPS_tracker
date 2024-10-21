from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le rotte

# Aggiungi altitude e speed al dizionario gps_data
gps_data = {
    'latitude': 0.0,
    'longitude': 0.0,
    'altitude': 0.0,  # Inizializza a 0.0 o a un valore predefinito
    'speed': 0.0  # Inizializza a 0.0 o a un valore predefinito
}


@app.route('/')
def index():
    return render_template('index_iphone.html')  # Servire l'HTML dalla cartella templates


@app.route('/update_coordinates', methods=['POST'])
def update_coordinates():
    global gps_data
    data = request.get_json()
    gps_data['latitude'] = data['latitude']
    gps_data['longitude'] = data['longitude']

    # Aggiungi altitude e speed se presenti nei dati inviati
    if 'altitude' in data:
        gps_data['altitude'] = data['altitude']
    if 'speed' in data:
        gps_data['speed'] = data['speed']

    return jsonify({'status': 'success', 'message': 'Coordinates updated'})


@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    return jsonify(gps_data)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)
