import tkinter as tk
from collections import deque
import random

class Cliente:
    def __init__(self, id_cliente, num_transacciones):
        self.id_cliente = id_cliente
        self.num_transacciones = num_transacciones

cola = deque()  # Crear la cola vacía


def generar_cliente(cola, max_transacciones=5):
    id_cliente = len(cola) + 1
    num_transacciones = random.randint(1, max_transacciones)
    nuevo_cliente = Cliente(id_cliente, num_transacciones)
    cola.append(nuevo_cliente)

def atender_cliente(cola):
    if cola:
        cliente_actual = cola.popleft()  # Sacar al cliente de la cola
        if cliente_actual.num_transacciones > 3:
            cliente_actual.num_transacciones -= 3
            cola.append(cliente_actual)  # Regresar al final de la cola
        else:
            print(f"Cliente {cliente_actual.id_cliente} atendido y retirado.")
    else:
        print("No hay clientes en la cola.")



class AplicacionBancaria:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulación Cajero Bancario")
        self.label = tk.Label(master, text="Estado de la Cola:")
        self.label.pack()

        self.boton_generar = tk.Button(master, text="Generar Cliente", command=self.agregar_cliente)
        self.boton_generar.pack()

        self.boton_atender = tk.Button(master, text="Atender Cliente", command=self.atender_cliente)
        self.boton_atender.pack()

        self.cola_display = tk.Label(master, text="")
        self.cola_display.pack()

    def agregar_cliente(self):
        generar_cliente(cola)
        self.mostrar_cola()

    def atender_cliente(self):
        atender_cliente(cola)
        self.mostrar_cola()

    def mostrar_cola(self):
        estado = ""
        for cliente in cola:
            estado += f"Cliente {cliente.id_cliente} - {cliente.num_transacciones} transacciones\n"
        self.cola_display.config(text=estado)

root = tk.Tk()
app = AplicacionBancaria(root)
root.mainloop()
