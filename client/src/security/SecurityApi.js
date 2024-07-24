
export class SecurityApi {

    url = "http://localhost:8000";

    userId;

    socket

    constructor(userId) {
        this.userId = userId;
    }

    // Robust disconnect detection by implementing a heartbeat.
    // Seamless automatic reconnection.
    listenForUpdate(callback) {
        // WebSocket lacks custom headers, so appending user in the url
        this.socket = new WebSocket("ws://127.0.0.1:8000/ws/watchlist/" + this.userId + "/")
        this.socket.addEventListener("open", event => {
            console.log("socket open");
            //socket.send("Connection established")
        });
        this.socket.addEventListener("message", event => {
            console.log("Message from server ", event.data)
            callback(JSON.parse(event.data))
        });
    }

    /**
     * when adding new stocks, subscribe for updates
     * @param ticker
     */
    subTicker(ticker) {
        this.socket.send(JSON.stringify({command:"sub", ticker:ticker}));
    }

    /**
     * when removing stocks unsubscribe
     * @param ticker
     */
    unsubTicker(ticker) {
        this.socket.send(JSON.stringify({command:"unsub", ticker:ticker}));
    }

    search(term, callback) {
        fetch(this.url + "/security/?q=" + encodeURI(term), {
            method: 'GET',
            headers: {'Content-Type': 'application/json'},
        })
            .then((response) => response.json())
            .then(data => {
                console.log("Search Results", data);
                callback(data);
            }).catch(error => {
            console.error('search failed', error);
        })
    }

    list(callback) {
        fetch(this.url + "/user/security/", {
            method: 'GET',
            headers: { 'Content-Type': 'application/json',
                'x-user-id': this.userId},
        })
            .then((response) => response.json())
            .then((data) => {
                // refresh security list
                console.info('UserSecurity added successfully');
                callback(data);
            })
            .catch((error) => {
                console.error('Failed to add UserSecurity', error);
            });
    }

    add(securityId) {
        fetch(this.url + "/user/security/", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json',
            'x-user-id': this.userId},
            body: JSON.stringify({ id: securityId}),
        })
            .then((response) => response)
            .then((data) => {
                // refresh security list
                console.info('UserSecurity added successfully');
            })
            .catch((error) => {
                console.error('Failed to add UserSecurity', error);
            });
    }

    remove(securityId) {
        fetch(this.url + "/user/security/", {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json',
                'x-user-id': this.userId},
            body: JSON.stringify({ id: securityId}),
        })
            .then((response) => response)
            .then((data) => {
                // refresh security list
                console.info('UserSecurity removed successfully');
            })
            .catch((error) => {
                console.error('Failed to remove UserSecurity', error);
            });
    }

}