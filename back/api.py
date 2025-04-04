import random
import time
from queue import Queue
import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir todas las solicitudes CORS


# Almacena los eventos de la simulación
eventos_simulacion = []

# Bandera para controlar si la simulación está activa o ha terminado
simulacion_activa = False

# Clase para representar un cliente
class Cliente:
    def __init__(self, id_cliente):
        self.id_cliente = id_cliente
        self.transacciones = random.randint(1, 5)  # Cada cliente tiene entre 1 y 5 transacciones

# Función para atender a los clientes en la cola
def atender_cliente(cliente):
    evento = {
        "cliente_id": cliente.id_cliente,
        "transacciones_restantes": cliente.transacciones,
        "estado": "atendiendo"
    }
    eventos_simulacion.append(evento)
    print(f"Atendiendo al cliente {cliente.id_cliente} con {cliente.transacciones} transacciones.")
    transacciones_atendidas = 0

    while cliente.transacciones > 0:
        if transacciones_atendidas == 3 and cliente.transacciones > 0:
            evento = {
                "cliente_id": cliente.id_cliente,
                "transacciones_restantes": cliente.transacciones,
                "estado": "volver_a_cola"
            }
            eventos_simulacion.append(evento)
            print(f"Cliente {cliente.id_cliente} debe volver a la cola. Le quedan {cliente.transacciones} transacciones.")
            return False  # El cliente vuelve al final de la cola

        cliente.transacciones -= 1
        transacciones_atendidas += 1
        evento = {
            "cliente_id": cliente.id_cliente,
            "transacciones_restantes": cliente.transacciones,
            "estado": "transaccion_procesada"
        }
        eventos_simulacion.append(evento)
        print(f"Procesada una transacción del cliente {cliente.id_cliente}. Transacciones restantes: {cliente.transacciones}")
        time.sleep(4)  # Simula el tiempo de procesamiento de una transacción

    evento = {
        "cliente_id": cliente.id_cliente,
        "transacciones_restantes": 0,
        "estado": "completado"
    }
    eventos_simulacion.append(evento)
    print(f"Cliente {cliente.id_cliente} ha completado todas sus transacciones.")
    return True  # El cliente ha terminado todas sus transacciones

# Simulación de la llegada de clientes y el procesamiento de la cola
def simulacion_banco():
    global simulacion_activa
    simulacion_activa = True  # La simulación está activa
    eventos_simulacion.clear()  # Limpiar los eventos previos
    cola = Queue()
    id_cliente = 1
    generaciones = 0

    while generaciones < 4 or not cola.empty():
        # Llegada aleatoria de nuevos clientes
        if generaciones < 4:
            nuevos_clientes = random.randint(0, 3)  # Pueden llegar entre 0 y 3 clientes nuevos
            for _ in range(nuevos_clientes):
                cliente = Cliente(id_cliente)
                evento = {
                    "cliente_id": id_cliente,
                    "transacciones": cliente.transacciones,
                    "estado": "nuevo_cliente"
                }
                eventos_simulacion.append(evento)
                print(f"Llega el cliente {id_cliente} con {cliente.transacciones} transacciones.")
                cola.put(cliente)
                id_cliente += 1
            generaciones += 1

        # Atender a los clientes en la cola
        if not cola.empty():
            cliente_actual = cola.get()
            if not atender_cliente(cliente_actual):
                cola.put(cliente_actual)  # Cliente vuelve al final de la cola si no terminó sus transacciones

        # Simula el tiempo entre llegadas y atención
        time.sleep(4)

    evento = {"estado": "simulacion_terminada"}
    eventos_simulacion.append(evento)
    print("La simulación ha terminado. No quedan más clientes en la cola.")
    simulacion_activa = False  # La simulación ha terminado


# Endpoint para obtener los eventos de la simulación
@app.route('/api', methods=['GET'])
def get_simulacion():
    return jsonify(eventos_simulacion)


# Endpoint para reiniciar la simulación
@app.route('/clients', methods=['POST'])
def reiniciar_simulacion():
    global simulacion_activa

    # Solo permitir reiniciar si la simulación ha terminado
    if simulacion_activa:
        return jsonify({"error": "La simulación aún está en curso, espera a que termine."}), 400

    # Reiniciar la simulación en un hilo separado
    simulacion_thread = Thread(target=simulacion_banco)
    simulacion_thread.start()

    return jsonify({"mensaje": "La simulación ha sido reiniciada."})


# Iniciar la simulación y servirla en Flask
if __name__ == "__main__":
    # Inicia la simulación en un hilo separado para que Flask pueda correr simultáneamente
    from threading import Thread
    simulacion_thread = Thread(target=simulacion_banco)
    simulacion_thread.start()

    # Inicia el servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
