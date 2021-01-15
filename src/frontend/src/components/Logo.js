import React from 'react';
import { useHistory } from 'react-router';

const Logo = () => {
    const history = useHistory();
    return (
        <div class='home-banner' onClick={() => history.push('/feed')}>
            <h1 style={{ cursor: 'pointer' }}>3tography</h1>
        </div>
    )
}

export default Logo;
