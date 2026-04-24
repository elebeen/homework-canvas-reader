const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());

// 1. Inicializar Cliente de WhatsApp
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { args: ['--no-sandbox'] } // Necesario para algunos servidores
});

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('Escanea el código QR de arriba para iniciar sesión.');
});

client.on('ready', () => {
    console.log('✅ WhatsApp Web está listo y conectado.');
});

// 2. Definir el Endpoint para enviar mensajes
app.post('/send-report', async (req, res) => {
    const { message, number } = req.body;

    if (!message || !number) {
        return res.status(400).json({ error: 'Faltan parámetros: message o number' });
    }

    try {
        const chatId = number.includes('@c.us') ? number : `${number}@c.us`;
        await client.sendMessage(chatId, message);
        console.log(`🚀 Reporte enviado a ${number}`);
        res.status(200).json({ success: true, message: 'Reporte enviado correctamente' });
    } catch (error) {
        console.error('❌ Error al enviar:', error);
        res.status(500).json({ error: 'No se pudo enviar el mensaje' });
    }
});

client.initialize();

app.listen(port, () => {
    console.log(`🌐 Servidor Express escuchando en http://localhost:${port}`);
});