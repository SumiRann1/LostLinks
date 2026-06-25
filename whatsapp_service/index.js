global.crypto = require('crypto').webcrypto;
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } = require('@whiskeysockets/baileys');
const express = require('express');
const qrcodeTerminal = require('qrcode-terminal');
const QRCode = require('qrcode');
const path = require('path');
const pino = require('pino');

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
let sock = null;
let isClientReady = false;

async function startSock() {
    console.log('Initializing Baileys WhatsApp client...');
    
    // Save authentication credentials in the local cache directory
    const { state, saveCreds } = await useMultiFileAuthState('./.baileys_auth');
    
    // Fetch latest version of WhatsApp Web protocol dynamically
    let version = [2, 3000, 1035194821]; // fallback version
    try {
        const fetched = await fetchLatestBaileysVersion();
        if (fetched && fetched.version) {
            version = fetched.version;
            console.log(`Using dynamically fetched WaWeb version: ${version.join('.')}`);
        }
    } catch (e) {
        console.warn('Failed to fetch latest Baileys version dynamically, using fallback:', e.message);
    }

    sock = makeWASocket({
        version,
        auth: state,
        printQRInTerminal: false,
        logger: pino({ level: 'silent' }) // suppress verbose logs
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;
        
        if (qr) {
            console.log('\n================================================================================');
            console.log('QR CODE RECEIVED! Saving image to whatsapp_service/qr.png...');
            console.log('================================================================================\n');
            
            qrcodeTerminal.generate(qr, { small: true });
            
            const targetPath = path.join(__dirname, 'qr.png');
            QRCode.toFile(targetPath, qr, { scale: 8 }, (err) => {
                if (err) console.error('Failed to save QR code PNG to:', targetPath, err);
                else console.log('Successfully saved QR code image to whatsapp_service/qr.png! Access it via the secure /whatsapp/qr.png route.');
            });
        }

        if (connection === 'close') {
            isClientReady = false;
            const statusCode = lastDisconnect?.error?.output?.statusCode;
            const shouldReconnect = statusCode !== DisconnectReason.loggedOut;
            console.error('Connection closed due to error:', lastDisconnect?.error);
            if (lastDisconnect?.error?.stack) {
                console.error(lastDisconnect.error.stack);
            }
            
            if (shouldReconnect) {
                setTimeout(startSock, 3000); // retry after 3 seconds
            }
        } else if (connection === 'open') {
            console.log('WhatsApp client is READY and connected!');
            isClientReady = true;
        }
    });
}

// Send message API route
app.post('/send-message', async (req, res) => {
    const { phone, message } = req.body;
    
    if (!phone || !message) {
        return res.status(400).json({ success: false, error: 'Phone and message are required.' });
    }

    if (!sock || !isClientReady) {
        return res.status(503).json({ success: false, error: 'WhatsApp client is not ready yet. Please scan the QR code to authenticate.' });
    }

    try {
        // Clean phone number (must be digits only)
        let cleanedPhone = phone.toString().replace(/[^0-9]/g, '');
        
        // Baileys JID format: phone@s.whatsapp.net
        const jid = `${cleanedPhone}@s.whatsapp.net`;
        
        console.log(`Sending message to ${jid}...`);
        
        const response = await sock.sendMessage(jid, { text: message });
        
        console.log(`Message successfully sent to ${jid}`);
        res.json({ success: true, messageId: response.key.id });
    } catch (err) {
        console.error('Error sending message:', err);
        res.status(500).json({ success: false, error: err.message || 'Failed to send message.' });
    }
});

// Health check endpoint
app.get('/status', (req, res) => {
    res.json({
        success: true,
        ready: isClientReady
    });
});

app.listen(PORT, () => {
    console.log(`WhatsApp Gateway Express server running on port ${PORT}`);
});

startSock().catch(err => console.error('Start Sock failure:', err));
