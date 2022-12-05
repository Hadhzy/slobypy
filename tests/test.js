// Write simple client websocket code
// Run: node test.js

var WebSocket = require('ws');
var ws = new WebSocket('ws://localhost:8765');

let last_sequence = null;

ws.on('open', async function open() {
    ws.send(JSON.stringify({
        "type": "identify",
        "data": {
            "id": 1,
            "client": "sloby A034",
            "max_shards": 10,
            "shards": {},
            "heartbeat_interval": 4500
        }
    }));
    await new Promise(r => setTimeout(r, 2000));
//    Simulate a new request
    ws.send(JSON.stringify({
        "type": "new_shard",
        "data": {
            "id": 1,
            "route": "/route1",
            "metadata": {
                "agent": "Chrome/108.0.0.0",
                "cookies": ["cookie1", "cookie2"],
                "ip_address": "192.168.1.1"
            },
        }
    }));
});

ws.on('message', async function (data, flags) {
    const message = JSON.parse(flags ? data : data.toString());
    console.log(message);
    if (message.type !== "heartbeatACK") {
        last_sequence = message.sequence;
    }
    if (message.type === "ready") {
        heartbeat();
    }

});

function heartbeat() {
    if (!ws) return;
    if (ws.readyState !== 1) return;
    ws.send(JSON.stringify({
        "type": "heartbeat",
        "data": {
            "sequence": last_sequence
        }
    }));
    setTimeout(heartbeat, 4500);
}