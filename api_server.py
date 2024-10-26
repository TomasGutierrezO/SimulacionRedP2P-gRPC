from flask import Flask, request, jsonify
from auth.auth_service import AuthService
import json

app = Flask(__name__)

auth_service = AuthService()

users_sessions = []

# Iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    if username in users_sessions:
        return jsonify({'message': 'El usuario ya ha iniciado sesión'}), 403
    elif auth_service.authenticate(username, password):
        users_sessions.append(username)
        return jsonify({'message': 'Sesión iniciada correctamente'}), 200
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401


# Cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    username = request.json['username']
    if username in users_sessions:
        users_sessions.remove(username)
        return jsonify({'message': 'Se ha cerrado sesión correctamente'}), 200
    return jsonify({'message': 'Usuario no encontrado'}), 404


# Archivos que tiene un peer
@app.route('/index', methods=['POST'])
def share_file():
    username = request.json.get('username')
    password = request.json.get('password')

    if not all([username, password]):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    if username == 'peer1':
        file_path = 'peer1/peer_config.json'
    elif username == 'peer2':
        file_path = 'peer2/peer_config.json'
    elif username == 'peer3':
        file_path = 'peer3/peer_config.json'
    elif username == 'peer4':
        file_path = 'peer4/peer_config.json'
    else: 
        return jsonify({"message": "Peer no encontrado"}), 404

    if auth_service.authenticate(username, password):
        with open(file_path) as f:
            data = json.load(f)
        
        files = data.get('files')
        peer = data.get('peer_id')

        try:
            with open('files_peer.json') as f:
                files_peer_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            files_peer_data = {}

        if peer not in files_peer_data:
            files_peer_data[peer] = {'files': files}
        else:
            if files_peer_data[peer]['files'] != files:
                files_peer_data[peer]['files'] = files

        with open('files_peer.json', 'w') as f:
            json.dump(files_peer_data, f, indent=4)

        return jsonify({"message": "Archivo guardado con éxito"}), 200
    else:
        return jsonify({"message": "Credenciales inválidas"}), 400


# Búqueda de peers que contienen archivos
with open('files_peer.json') as f:
    peer_list = json.load(f)

def buscar_peers(file_name):
    peers = []
    for peer_id, peer_info in peer_list.items():
        if file_name in peer_info['files']:
            peers.append({
                'peer_id': peer_id,
                'ip': peer_info['ip'],
                'port': peer_info['port']
            })

    return peers

@app.route('/search', methods=['GET'])
def search_file():
    file_name = request.args.get('file_name')
    if file_name is None:
        return jsonify({'error': 'No se proporcionó el nombre del archivo'}), 400

    peers = buscar_peers(file_name)
    if not peers:
        return jsonify({'error': 'No se encontraron peers con el archivo'}), 404

    return jsonify({'peers': peers})


@app.route('/download', methods=['POST'])
def download_file():
    username = request.json.get('username')
    password = request.json.get('password')
    file_name = request.json.get('file_name')

    if not all([username, password, file_name]):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    if auth_service.authenticate(username, password):
        with open('files_peer.json') as f:
            files_peer_data = json.load(f)

        for peer_id, peer_info in files_peer_data.items():
            if file_name in peer_info['files']:
                # Aquí obtenemos la configuración del peer
                with open(f"{peer_id}/peer_config.json") as peer_f:
                    peer_config = json.load(peer_f)

                return jsonify({
                    "peer_id": peer_id,
                    "ip": peer_config['ip'],
                    "port": peer_config['port'],
                    "message": "Archivo encontrado"
                }), 200

        return jsonify({"message": "Archivo no encontrado en ningún peer"}), 404
    else:
        return jsonify({"message": "Credenciales inválidas"}), 400

if __name__ == '__main__':
    app.run(debug=True)