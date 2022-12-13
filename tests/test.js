// Write simple client websocket code
// Run: node test.js

var WebSocket = require('ws');
var ws = new WebSocket('ws://localhost:8765');

// var express = require('express');
//
// var app = express();
// app.use(express.static("demo_server_static"));
//
// app.get('/', function (req, res) {
//     res.send('<link type="text/css" href="css/styles.css" rel="stylesheet">\n' + html);
// });

let last_sequence = null;
let html = '';
let css = '';

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
    if (message.type === "update_shard_data") {
        console.log("Update shard data");
        html = message.data.html;
    //    Store the css in a style.css file
        css = message.data.css;
        // fs.writeFile('demo_server_static/css/style.css', css, function (err) {
        //     if (err) throw err;
        //     console.log('CSS Saved!');
        // });
    }
    if (message.type === "heartbeat") {
        console.log("Sending heartbeat FORCE");
        ws.send(JSON.stringify({
            "type": "heartbeat",
            "data": {
                "sequence": last_sequence
            }
        }));
    }
});

function heartbeat() {
    if (!ws) return;
    if (ws.readyState !== 1) return;
    console.log("Sending heartbeat");
    ws.send(JSON.stringify({
        "type": "heartbeat",
        "data": {
            "sequence": last_sequence
        }
    }));
    setTimeout(heartbeat, 4500);
}

// app.listen(8081, function () {
//
// console.log('Demo Sloby Web Application is UP on port 8081');
//
// });