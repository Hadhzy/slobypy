// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:8081/refresh');

// Listen for messages
socket.addEventListener('message', (event) => {
    if (event.data === "refresh") {
        //    Refresh the page
        location.reload();
    }
});