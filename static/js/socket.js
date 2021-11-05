function socket_connect(url) {

    let socket = new WebSocket(
        `ws://${url}`
    );

    socket.onclose = (e) => {
        console.error('Chat socket closed unexpectedly');
    };

    return socket
}

