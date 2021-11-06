async function ajaxCall(url, method, data, _hearders) {


    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            ..._hearders
        },
        body: method == "POST" ? JSON.stringify(data) : null
    });

    return response;
}