function send_message() {
    const { createSocket } = require('dgram');
    const client = createSocket('udp4');

    client.send(document.getElementById('message').value, 56789, (error) => {
        client.close();
    });
}