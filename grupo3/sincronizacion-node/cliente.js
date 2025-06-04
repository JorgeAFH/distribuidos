// cliente.js
const axios = require('axios');

// URL del servidor
const URL_SERVIDOR = 'http://localhost:5050/hora';

// Función para sincronizar la hora
async function sincronizarHora() {
    try {
        const T0 = Date.now(); // Tiempo antes de la solicitud

        const respuesta = await axios.get(URL_SERVIDOR);
        const T1 = Date.now(); // Tiempo después de recibir respuesta

        const horaServidor = new Date(respuesta.data);
        const retardoRed = (T1 - T0) / 2; // En milisegundos
        const horaSincronizada = new Date(horaServidor.getTime() + retardoRed);

        const horaLocal = new Date();

        // Calcular diferencia entre la hora sincronizada y la hora local
        const diferencia = Math.abs(horaSincronizada.getTime() - horaLocal.getTime()) / 1000; // en segundos

        console.log("⏰ RESULTADOS DE SINCRONIZACIÓN");
        console.log("Hora local del cliente:       ", horaLocal.toISOString());
        console.log("Hora recibida del servidor:   ", horaServidor.toISOString());
        console.log("Hora ajustada (sincronizada):", horaSincronizada.toISOString());
        console.log("📶 Retardo estimado de red:     ", (retardoRed / 1000).toFixed(6), "segundos");
        console.log("📊 Diferencia local vs sincronizada:", diferencia.toFixed(6), "segundos");

    } catch (error) {
        console.error("❌ Error al sincronizar:", error.message);
    }
}

// Ejecutar
sincronizarHora();
