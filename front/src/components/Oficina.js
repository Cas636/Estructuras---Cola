import React, { useEffect, useState } from "react";
import cajero from "../images/cajero.png";
import cliente from "../images/cliente.png";
import atendiendo from "../images/atendiendo.png";

const OficinaBanco = () => {
  const [clients, setClients] = useState([]);

  // Función para procesar los clientes
  const procesarClientes = (data) => {
    const clientesTemp = {};

    data.forEach((registro) => {
      const { cliente_id, estado, transacciones, transacciones_restantes } = registro;
      

      // Si el cliente no existe en el estado temporal, lo creamos
      if (cliente_id && !clientesTemp[cliente_id]) {
        clientesTemp[cliente_id] = {
          cliente_id,
          estado: 'nuevo_cliente',
          transacciones: transacciones || 0,
          transacciones_restantes: transacciones || 0,
        };
      }

      // Si ya existe, actualizamos el estado del cliente
      if (cliente_id) {
        const clienteActual = clientesTemp[cliente_id];

        // Actualizar el estado y transacciones restantes
        clienteActual.estado = estado;
        if (transacciones_restantes !== undefined) {
          clienteActual.transacciones_restantes = transacciones_restantes;
        }
      }
    });

    // Retornar los clientes procesados como un array
    return Object.values(clientesTemp);
  };

  // Obtener datos de la oficina al cargar el componente
  useEffect(() => {
    const fetchOficina = async () => {
      try {
        const response = await fetch("http://localhost:5000/api"); // Cambia la URL según tu API
        const data = await response.json();
       
        // Crear un mapa para almacenar el último estado de cada cliente por su id
      const clientesActualizados = {};

      // Iterar sobre los datos y actualizar el cliente más reciente basado en `cliente_id`
      data.forEach((cliente) => {
        clientesActualizados[cliente.cliente_id] = cliente;
      });
      console.log(clientesActualizados);
      
      // Convertir el objeto en un array de clientes únicos
      let clientesFiltrados = Object.values(clientesActualizados);

      // Filtrar clientes que tienen 0 transacciones restantes o Si está siendo atendido 
      clientesFiltrados = clientesFiltrados.filter((cliente) => {
        return (
          cliente.estado !== "completado" || cliente.estado !== "simulacion_terminada" || cliente.transacciones_restantes > 0 
        );
      });

      // Actualizar el estado con los clientes filtrados
      console.log(clientesFiltrados);
      setClients(clientesFiltrados);
      } catch (error) {
        console.error("Error al obtener la oficina:", error);
      }
    };

    // Establecer un intervalo que actualice los datos cada 1 segundo (1000 ms)
    const intervalId = setInterval(fetchOficina, 100);

    // Limpiar el intervalo cuando el componente se desmonte
    return () => clearInterval(intervalId);
  }, []);

  // Método para incrementar la cantidad de clientes
  const incrementarClientes = async () => {
    try {
      const response = await fetch("http://localhost:5000/clients", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const nuevosClientes = await response.json();
        console.log(nuevosClientes);
      } else {
        console.error("Error al incrementar los clientes:", response.statusText);
      }
    } catch (error) {
      console.error("Error en la solicitud:", error);
    }
  };

  const renderClienteAtendido = () => {
    return clients
      .filter((client) => client.estado === "atendiendo" || client.estado === "transaccion_procesada")
      .map((client) => (
        <div
          key={client.cliente_id}
          style={{ marginRight: "10px", textAlign: "center" }}
        >
          <img
            src={atendiendo}
            alt={`Cliente ${client.cliente_id}`}
            style={{ display: "block", marginBottom: "5px" }}
          />
          <div>Cliente ID: {client.cliente_id}</div>
          <div>Transacciones Restantes: {client.transacciones_restantes}</div>
          <div>Transacciones Restantes: {client.estado}</div>
        </div>
      ));
  };

  const renderClientes = () => {
    return clients.map((client) => (
      <div
        key={client.cliente_id}
        style={{ marginRight: "10px", textAlign: "center" }}
      >
        <img
          src={cliente}
          alt={`Cliente ${client.cliente_id}`}
          style={{ display: "block", marginBottom: "5px" }}
        />
        <div>Cliente ID: {client.cliente_id}</div>
        <div>Transacciones Restantes: {client.transacciones_restantes}</div>
        <div>Transacciones Restantes: {client.estado}</div>
      </div>
    ));
  };

  return (
    <div>
      <h1>Oficina Bancaria</h1>
      <p>Cantidad de clientes actuales: {clients.length}</p>
      <button onClick={incrementarClientes}>Iniciar Proceso</button>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "flex-end",
        }}
      >
        <div style={{ display: "flex", flexDirection: "row-reverse" }}>
          {renderClientes()}
        </div>

        <div style={{ display: "flex" }}>{renderClienteAtendido()}</div>
        
        <img
          src={cajero}
          alt="Cajero automático"
          style={{ marginRight: "20px" }}
        />
      </div>
    </div>
  );
};

export default OficinaBanco;
