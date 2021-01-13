import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import './styles/Card.css';
import Auth from '../utils/auth';

const Register = () => {

    const [credentials, setCredentials] = useState({});
    const history = useHistory();

    const handleSubmit = async event => {
        event.preventDefault();
        try {
            if (!credentials.user || !credentials.password) {
                return;
            }
            if (await Auth.register(credentials.user, credentials.password)) {
                history.push('/login')
            }
        } catch (err) {
            console.error(err);
        }
    }

    useEffect(async () => {
        if (await Auth.isLoggedIn()) {
            history.push('/me')
        }
    }, []);


    return (
        <>
            <div className='container'>
                <div className='card'>
                    <h1>Register</h1>
                    <form onSubmit={handleSubmit} >
                        <input type='text' onChange={event => setCredentials({...credentials, user: event.target.value})} placeholder='Please enter your username'></input>
                        <input type='password' onChange={event => setCredentials({...credentials, password: event.target.value})} placeholder='Please enter your password'></input>
                        <input type='submit' value='Register'></input>
                    </form>
                    <p>Already have an account? Login here</p>
                </div>
            </div>        
        </>
    )
}

export default Register;
