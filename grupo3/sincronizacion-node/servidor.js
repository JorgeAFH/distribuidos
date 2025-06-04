// servidor.js
const express = require('express');
const app = express();
const PORT = 5050;

app.use(express.static('public'));

app.get('/hora', (req, res) => {
    const horaActual = new Date().toISOString();
    res.send(horaActual);
});

app.listen(PORT, () => {
    console.log(`🌐 Servidor corriendo en http://localhost:${PORT}`);
});
