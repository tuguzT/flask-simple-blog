function post_json(url, json) {
    const init = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(json),
    };
    return fetch(url, init);
}
