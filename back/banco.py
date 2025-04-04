from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import random
import time
from collections import deque
from threading import Thread, Event

app = Flask(__name__)
CORS(app)  # Permitir todas las solicitudes CORS

# Cola para manejar clientes
client_queue = deque()
max_transactions = 5
max_generations = 20
generations_count = 0
client_served = Event()   # Evento para indicar que un cliente ha sido atendido

class Client:
    def __init__(self, client_id):
        self.client_id = client_id
        self.transactions = 0

# Proceso para atender clientes
def serve_clients():
    global generations_count
    while generations_count < max_generations:
        if client_queue:
            client = client_queue.popleft()
            print(f"Atendiendo a Cliente {client.client_id}")

            # Simulación de la atención al cliente
            while client.transactions < max_transactions:
                # Simular que se recibe una transacción
                client.transactions += 1
                print(f"Cliente {client.client_id} ha realizado {client.transactions} transacciones.")
                time.sleep(1)  # Simula el tiempo de atención por transacción

            if client.transactions > max_transactions:
                # Si supera el máximo de transacciones, vuelve al final de la cola
                client_queue.append(client)
                print(f"Cliente {client.client_id} ha superado las transacciones y vuelve al final de la cola.")
            else:
                print(f"Cliente {client.client_id} ha sido atendido completamente y se retira.")
            
            client_served.set()  # Señaliza que un cliente ha sido atendido
        else:
            time.sleep(1)  # Esperar si no hay clientes en la cola

# Agregar clientes
@app.route('/add_client', methods=['POST'])
def add_client():
    global generations_count
    if generations_count < max_generations:
        client_id = len(client_queue) + 1  # Asignar un ID único al cliente
        client_queue.append(Client(client_id))
        print(f"Cliente {client_id} ha llegado a la cola.")
        
        # Incrementar el contador de generaciones si se añade un cliente
        if not client_served.is_set():
            generations_count += 1
        
        return jsonify({"message": f"Cliente {client_id} añadido a la cola."}), 201
    else:
        return jsonify({"message": "Límite de generaciones alcanzado."}), 400

# Ruta para Server-Sent Events (SSE)
@app.route('/events', methods=['GET'])
def stream():
    def event_stream():
        while True:
            time.sleep(1)  # Simulación del tiempo entre eventos
            if client_queue:
                # Enviar el estado de la cola y los clientes
                clients_status = []
                for client in client_queue:
                    clients_status.append({
                        "client_id": client.client_id,
                        "transactions": client.transactions
                    })
                
                yield f"data: {jsonify({'clients_in_queue': len(client_queue), 'clients': clients_status}).get_data(as_text=True)}\n\n"
            else:
                yield "data: No hay clientes en la cola.\n\n"

    return Response(event_stream(), mimetype='text/event-stream')

# Obtener el estado actual de la cola
@app.route('/status', methods=['GET'])
def get_status():
    clients_status = []
    
    # Iterar sobre la cola de clientes
    for client in client_queue:
        clients_status.append({
            "client_id": client.client_id,
            "transactions": client.transactions
        })
    
    return jsonify({"clients_in_queue": len(client_queue), "clients": clients_status}), 200


if __name__ == '__main__':
    # Iniciar el hilo para atender clientes
    Thread(target=serve_clients, daemon=True).start()
    # Iniciar el servidor Flask en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
