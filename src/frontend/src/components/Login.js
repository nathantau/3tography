import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import './styles/Card.css';
import Auth from '../utils/auth';


const Login = () => {

    const [credentials, setCredentials] = useState({});
    const history = useHistory();

    const handleSubmit = async event => {
        event.preventDefault();
        try {
            if (!credentials.user || !credentials.password) {
                return;
            }
            await Auth.login(credentials.user, credentials.password);
            if (await Auth.isLoggedIn()) {
                history.push('/')
            }
        } catch (err) {
            console.error(err);
        }
    }

    useEffect(() => {
        if (Auth.authenticated) {
            history.push('/');
        }
    }, [history]);

    return (
        <>
            <div className='container'>
                <div className='prompt-card card'>
                    <h1>Login</h1>
                    <form onSubmit={handleSubmit} >
                        <input type='text' onChange={event => setCredentials({...credentials, user: event.target.value})} placeholder='Please enter your username'></input>
                        <input type='password' onChange={event => setCredentials({...credentials, password: event.target.value})} placeholder='Please enter your password'></input>
                        <input type='submit' value='Login'></input>
                    </form>
                    <p>Don't have an account? Register here</p>
                </div>
            </div>        
        </>
    )
}

export default Login;
