const host = 'http://localhost:5000';
const Auth = {
    authenticated: false,
    init: async () => {
        try {
            Auth.authenticated = await Auth.isLoggedIn();
        } catch (err) {
            console.error(err);
        }
    },
    login: async (username, password) => {
        try {
            let res = await fetch(`${host}/login`, {
                method: 'POST',
                body: JSON.stringify({
                    user: username,
                    password: password
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            res = await res.json();
            if (res.success && res.accessToken) {
                localStorage.setItem('3tography-access-token', res.accessToken);
            }
        } catch (err) {
            console.error(err);
            Auth.logout();
        }
    },
    logout: () => {
        localStorage.clear();
    },
    isLoggedIn: async () => {
        try {
            const token = localStorage.getItem('3tography-access-token');
            if (!token) {
                return false;
            }
            let res = await fetch(
                `${host}/authenticated`, {
                    headers: {
                        Authorization: 'Bearer ' + token
                    }
                }
            );
            res = await res.json();
            if (res.authenticated) {
                return true;
            }
        } catch (err) {
            console.error(err);
        }
        return false;
    }
}

export default Auth
