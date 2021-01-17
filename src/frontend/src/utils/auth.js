const host = process.env.REACT_APP_FLASK_HOST;

const Auth = {
    authenticated: localStorage.getItem('3tography-access-token'),
    init: async () => {
        try {
            Auth.authenticated = await Auth.isLoggedIn();
        } catch (err) {
            console.error(err);
        }
    },
    login: async (username, password) => {
        try {
            let res = await fetch(`${host}/api/login`, {
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
            if (res.accessToken) {
                localStorage.setItem('3tography-access-token', res.accessToken);
                Auth.authenticated = true;
            }
        } catch (err) {
            console.error(err);
        }
    },
    register: async (username, password) => {
        /**
         * Returns 'true' if successfully registered, 'false' otherwise
         */
        try {
            let res = await fetch(`${host}/api/register`, {
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
            return res.registered;
        } catch (err) {
            console.error(err);
        }
        return false; 
    },
    logout: history => {
        Auth.authenticated = false;
        localStorage.removeItem('3tography-access-token');
        if (history) {
            history.push('/login')
        }
    },
    isLoggedIn: async () => {
        try {
            const token = localStorage.getItem('3tography-access-token');
            if (!token) {
                return false;
            }
            let res = await fetch(
                `${host}/api/authenticated`, {
                    headers: {
                        Authorization: 'Bearer ' + token
                    }
                }
            );
            res = await res.json();
            console.log('authenticated', res)
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
