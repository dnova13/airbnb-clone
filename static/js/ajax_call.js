async function ajaxCall(url, method, data) {

    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
        },
        body: method == "POST" ? JSON.stringify(data) : null
    });

    return response;
}