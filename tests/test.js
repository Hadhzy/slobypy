// Write simple client websocket code
// Run: node test.js

var WebSocket = require('ws');
var ws = new WebSocket('ws://localhost:8765');

let last_sequence = null;

ws.on('open', function open() {
    ws.send(JSON.stringify({
        "type": "identify",
        "data": {
            "id": 1,
            "client": "sloby A034",
            "max_shards": 10,
            "shards": ["shard1", "shard2", "shard3"],
            "heartbeat_interval": 4500
        }
    }));
});

ws.on('message', function (data, flags) {
    const message = JSON.parse(flags ? data : data.toString());
    console.log(message);
    if (message.type === "ready") {
        last_sequence = message.sequence;
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