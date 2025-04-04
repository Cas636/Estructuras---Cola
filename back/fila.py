import random
import time
from queue import Queue

# Clase para representar un cliente
class Cliente:
    def __init__(self, id_cliente):
        self.id_cliente = id_cliente
        self.transacciones = random.randint(1, 5)  # Cada cliente tiene entre 1 y 5 transacciones

# Función para atender a los clientes en la cola
def atender_cliente(cliente):
    print(f"Atendiendo al cliente {cliente.id_cliente} con {cliente.transacciones} transacciones.")
    transacciones_atendidas = 0

    while cliente.transacciones > 0:
        if transacciones_atendidas == 3 and cliente.transacciones > 0:
            print(f"Cliente {cliente.id_cliente} debe volver a la cola. Le quedan {cliente.transacciones} transacciones.")
            return False  # El cliente vuelve al final de la cola

        cliente.transacciones -= 1
        transacciones_atendidas += 1
        print(f"Procesada una transacción del cliente {cliente.id_cliente}. Transacciones restantes: {cliente.transacciones}")
        time.sleep(1)  # Simula el tiempo de procesamiento de una transacción

    print(f"Cliente {cliente.id_cliente} ha completado todas sus transacciones.")
    return True  # El cliente ha terminado todas sus transacciones

# Simulación de la llegada de clientes y el procesamiento de la cola
def simulacion_banco():
    cola = Queue()
    id_cliente = 1
    generaciones = 0

    while generaciones < 4 or not cola.empty():
        # Llegada aleatoria de nuevos clientes
        if generaciones < 4:
            nuevos_clientes = random.randint(0, 3)  # Pueden llegar entre 0 y 3 clientes nuevos
            for _ in range(nuevos_clientes):
                cliente = Cliente(id_cliente)
                cola.put(cliente)
                print(f"Llega el cliente {id_cliente} con {cliente.transacciones} transacciones.")
                id_cliente += 1
            generaciones += 1

        # Atender a los clientes en la cola
        if not cola.empty():
            cliente_actual = cola.get()
            if not atender_cliente(cliente_actual):
                cola.put(cliente_actual)  # Cliente vuelve al final de la cola si no terminó sus transacciones

        # Simula el tiempo entre llegadas y atención
        time.sleep(2)

    print("La simulación ha terminado. No quedan más clientes en la cola.")

# Ejecutar la simulación
if __name__ == "__main__":
    simulacion_banco()
