import json
import sys
import os
import grpc 
import requests

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proto import p2p_pb2, p2p_pb2_grpc 

class P2PClient:
    def __init__(self):
        with open("peer_config.json") as f:
            data = json.load(f)
            self.peer_id = data["peer_id"]
            self.ip = data["ip"]
            self.port = data["port"]
            self.files = data["files"]
            self.api_url = f"http://127.0.0.1:5000/"
        
    def login(self):
        username = input("Ingrese su nombre de usuario (peer_id): ")
        password = input("Ingrese su contraseña: ")
        response = requests.post(self.api_url + "login", json={"username": username, "password": password})
        if response.status_code == 200:
            return {'message': 'Sesión iniciada correctamente'}
        return {'Error': 'Ha ocurrido un error iniciando sesión'}

    def logout(self):
        username = input("Ingrese su nombre de usuario (peer_id): ")
        response = requests.post(self.api_url + "logout", json={"username": username})
        if response.status_code == 200:
            return {'message': 'Sesión cerrada correctamente'}
        return {'Error': 'Ha ocurrido un error cerrando sesión'}

    def index(self):
        username = input("Ingrese su nombre de usuario (peer_id): ")
        password = input("Ingrese su contraseña: ")
        response = requests.post(self.api_url + "index", json={"username": username, "password": password})
        if response.status_code == 200:
            return {'message': 'Se han actualizado los archivos del peer'}
        return {'Error': 'Ha ocurrido un error actualizando los archivos del peer'}

    def search(self):
        """Busca un archivo en la red de peers y almacena los peers que lo tienen."""
        file_name = input("Ingrese el nombre del archivo que desea buscar: ")
        response = requests.get(self.api_url + "search", params={"file_name": file_name})
        if response.status_code == 200:
            peers = response.json()["peers"]
            self.available_peers = []
            for peer in peers:
                channel = grpc.insecure_channel(f"{peer['ip']}:{peer['port']}")
                stub = p2p_pb2_grpc.P2PServiceStub(channel)
                request = p2p_pb2.FileRequest(peer_id=self.peer_id, file_name=file_name)

                file_response = stub.GetFiles(request)
                if file_name in file_response.files:
                    print(f"Peer {peer['peer_id']} tiene el archivo '{file_name}'.")
                    print(f"IP: {peer['ip']}, Puerto: {peer['port']}")
                    self.available_peers.append(peer)
            if not self.available_peers:
                print("No se encontraron peers con ese archivo.")
        else:
            print("Error al buscar el archivo.")

    def download(self):
        """Solicita el nombre del archivo que el usuario desea descargar y lo transfiere."""
        if not self.available_peers:
            print("No hay peers disponibles con el archivo. Realice una búsqueda primero.")
            return

        file_name = input("Ingrese el nombre del archivo que desea descargar: ")

        print("Peers disponibles:")
        for idx, peer in enumerate(self.available_peers):
            print(f"{idx + 1}. Peer {peer['peer_id']} - IP: {peer['ip']}, Puerto: {peer['port']}")

        peer_idx = int(input("Seleccione el número del peer desde el cual desea descargar el archivo: ")) - 1
        if 0 <= peer_idx < len(self.available_peers):
            peer = self.available_peers[peer_idx]
            self.transfer_file(peer, file_name)
        else:
            print("Selección inválida.")

    def transfer_file(self, peer, file_name):
        """Función que se encarga de transferir un "archivo" (nombre del archivo) de un peer a otro."""
        channel = grpc.insecure_channel(f"{peer['ip']}:{peer['port']}")
        stub = p2p_pb2_grpc.P2PServiceStub(channel)
        
        request = p2p_pb2.FileRequest(peer_id=self.peer_id, file_name=file_name)
        
        download_response = stub.DownloadFile(request)
        
        if download_response.file_name:
            print(f"Archivo '{download_response.file_name}' recibido de Peer {peer['peer_id']}.")
            self.files.append(download_response.file_name)
            print(f"El archivo '{download_response.file_name}' ha sido añadido a tu lista de archivos.")
            self.save_files()
        else:
            print(f"El archivo '{file_name}' no está disponible para descargar en este peer.")

    def save_files(self):
        """Guarda los archivos actuales en peer_config.json."""
        with open("peer_config.json", "r") as f:
            data = json.load(f)
        data['files'] = self.files
        with open("peer_config.json", "w") as f:
            json.dump(data, f, indent=4)

def main():
    peer = P2PClient()
    
    while True:
        print("\nSeleccione una opción:")
        print("1. Login")
        print("2. Logout")
        print("3. Indexar archivos")
        print("4. Buscar archivo")
        print("5. Descargar archivo")
        print("6. Salir")
        opcion = input("Ingrese el número de la opción que desea ejecutar: ")

        if opcion == "1":
            resultado = peer.login()
            print(resultado)
        elif opcion == "2":
            resultado = peer.logout()
            print(resultado)
        elif opcion == "3":
            resultado = peer.index()
            print(resultado)
        elif opcion == "4":
            peer.search()
        elif opcion == "5":
            peer.download()
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
