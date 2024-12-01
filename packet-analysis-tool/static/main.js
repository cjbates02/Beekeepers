document.addEventListener("DOMContentLoaded", () => {
    websocket = io('http://127.0.0.1:5000');

    websocket.on('connect', () => {
        console.log('Connected to flask socket io server.');
    });

    websocket.on('packet', (data) => { 
        const packet = data.packet;
        console.log(packet);
    });
});