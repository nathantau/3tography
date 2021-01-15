import React from 'react';
import { useHistory } from 'react-router';
import './styles/User.css'

const Logo = () => {

    const history = useHistory();

    // onClick={() => Auth.logout(history)}

    return (
        <div class='home-banner' onClick={() => history.push('/feed')}>
            <h1>3tography</h1>
        </div>
    )
}

export default Logo;
