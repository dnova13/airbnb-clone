function socket_connect(url) {

    let wsStart = `ws://`

    if (window.location.protocol == 'https:') {
        wsStart = 'wss://'
    }

    let socket = new WebSocket(
        `${wsStart}${url}`
    );

    socket.onclose = (e) => {
        console.error('Socket closed unexpectedly');
    };

    return socket
}

