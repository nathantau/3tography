import React from 'react';
import User from './User';
import './styles/Home.css';

const Home = () => {
    return (
        <>
            <div class='home-banner'>
                <h1>3tography</h1>
            </div>
            <User username='sam'></User>
        </>
    )
}

export default Home;