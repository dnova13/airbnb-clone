function socket_connect(url) {

    let socket = new WebSocket(
        `ws://${url}`
    );

    socket.onclose = (e) => {
        console.error('Socket closed unexpectedly');
    };

    return socket
}

