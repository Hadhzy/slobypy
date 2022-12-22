// Write simple client websocket code
// Run: node test.js

var WebSocket = require('ws');
var ws = new WebSocket('ws://localhost:8765');
var fs = require('fs');

var express = require('express');
var app = express();
var expressWs = require('express-ws')(app);
var ips = [];
var html_hooks = [];

app.use(express.static("demo_server_static"));
app.set('etag', false)

// app.get('/', function (req, res) {
//     res.send(css_link + js_link + html);
// });

app.ws('/refresh', function (ws, req) {
});

app.get('*', async (req, res) => {
    if (req.originalUrl === "/favicon.ico") {
        res.send("");
        return;
    }
    if (!ips.includes(req.ip)) {
        let current_len = ips.length;
        ips.push(req.ip);
        html[ips.length] = {}
        html[ips.length].route = req.url
        html_hooks.push(function hook(message) {
            if (message.type === "update_shard_data") {
                console.log("hook")
                if (message.data.id === current_len + 1) {
                    res.send(css_link + js_link + message.data.html.replace("className", "class"));
                }
                //    Remove hook
                html_hooks.splice(html_hooks.indexOf(this.hook), 1);
            }
        })
        console.log("New IP: " + req.ip);
        ws.send(JSON.stringify({
            "type": "new_shard",
            "data": {
                "id": ips.length,
                "route": req.url,
                "metadata": {
                    "agent": req.userAgent,
                    "cookies": req.cookies,
                    "ip_address": req.ip
                },
            }
        }));
    } else {
        let html_data = html[ips.indexOf(req.ip) + 1]
        if (html_data.route !== req.url) {
            html_data.route = req.url;
            html_hooks.push(function hook(message) {
                if (message.type === "update_shard_data") {
                    console.log("hook")
                    if (message.data.id === ips.indexOf(req.ip) + 1) {
                        res.send(css_link + js_link + message.data.html.replace("className", "class"));
                    }
                    //    Remove hook
                    html_hooks.splice(html_hooks.indexOf(this.hook), 1);
                }
            })
            ws.send(JSON.stringify({
                "type": "get_route",
                "data": {
                    "id": ips.indexOf(req.ip) + 1,
                    "route": req.url,
                },
                "sequence": last_sequence
            }));
        } else {
            res.send(css_link + js_link + html_data.data);
        }
    }
});

var client_ws = expressWs.getWss('/refresh');
let last_sequence = null;
let html = {};
let css = '';
let css_link = "<link type=\"text/css\" href=\"css/style.css\" rel=\"stylesheet\">";
let js_link = "<script src=\"js/script.js\"></script>";

ws.on('open', async function open() {
    ws.send(JSON.stringify({
        "type": "identify",
        "data": {
            "client": "sloby A034",
            "max_shards": 10,
            "shards": {},
            "heartbeat_interval": 4500
        }
    }));
    await new Promise(r => setTimeout(r, 2000));
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
        html[message.data.id].data = message.data.html.replaceAll("className", "class");
        console.log(html);
        //    Store the css in a style.css file
        // css = message.data.css;
        // fs.writeFile('demo_server_static/css/style.css', css, function (err) {
        //     if (err) throw err;
        //     console.log('CSS Saved!');
        // });
        client_ws.clients.forEach(function (client) {
            console.log("Sending refresh message");
            client.send('refresh');
        });
        for (let hook of html_hooks) {
            hook(message);
        }
    }
    if (message.type === "reload_css") {
        //    Store the css in a style.css file
        css = message.data.css;
        fs.writeFile('demo_server_static/css/style.css', css, function (err) {
            if (err) throw err;
            console.log('CSS Saved!');
        });
        client_ws.clients.forEach(function (client) {
            console.log("Sending refresh message");
            client.send('refresh');
        });
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

app.listen(port = 8081, function () {

    console.log('Demo Sloby Web Application is UP on port', this.address().port);

});