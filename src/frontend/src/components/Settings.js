import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import './styles/Card.css';
import Auth from '../utils/auth';

const host = process.env.REACT_APP_FLASK_HOST;

const Settings = () => {

    const history = useHistory();
    const [description, setDescription] = useState('');
    const [candidate, setCandidate] = useState('');

    const fetchUser = async () => {
        try {
            let userInfo = await fetch(`${host}/api/me`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('3tography-access-token')}`
                }
            });
            userInfo = await userInfo.json();
            if (userInfo) {
                setDescription(userInfo.description);
            }
        } catch (err) {
            console.err(err);
        }
    }

    const handleSubmit = async event => {
        event.preventDefault();
        try {
            if (!candidate) {
                return;
            }
            const res = await fetch(`${host}/api/description`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('3tography-access-token')}`,
                    'Content-type': 'application/json'
                },
                body: JSON.stringify({
                    description: candidate
                })
            })
                .then(res => res.json());
            if (res.updated) {
                setDescription(candidate);
            }
        } catch (err) {
            console.error(err);
        }
    }

    useEffect(() => {
        const fetchData = async () => {
            if (!await Auth.isLoggedIn()) {
                history.push('/login');
            }
            await fetchUser();
        }
        fetchData();
    }, [history]);

    return (
        <>
            <div className='container'>
                <div className='prompt-card card'>
                    <h1>Description</h1>
                    <p>{description}</p>
                    <form onSubmit={handleSubmit} >
                        <input type='text' onChange={event => setCandidate(event.target.value)} placeholder='Please enter a description'></input>
                        <input type='submit' value='Update'></input>
                    </form>
                </div>
            </div>
        </>
    )
}

export default Settings;
