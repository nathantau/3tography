import React, { useEffect } from 'react';
import User from './User';
import './styles/Home.css';
import Auth from '../utils/auth';
import { useHistory } from 'react-router';

const Me = () => {

    const history = useHistory();

    useEffect(() => {
        const checkLoggedIn = async () => {
            if (!await Auth.isLoggedIn()) {
                history.push('/login');
            }
        }
        checkLoggedIn();
    }, []);

    return (
        <>
            <User></User>
        </>
    )
}

export default Me;