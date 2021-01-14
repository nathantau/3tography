import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import './styles/User.css'
import Auth from '../utils/auth';

const Logo = () => {

    const history = useHistory();

    return (
        <div class='home-banner' onClick={() => Auth.logout(history)}>
            <h1>3tography</h1>
        </div>
    )
}

export default Logo;
