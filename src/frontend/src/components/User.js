import React, { useEffect, useRef, useState } from 'react';
import Following from './Following';
import Image from './Image';
import './styles/User.css'

const User = () => {

    const [username, setUsername] = useState('');
    const [imageUrls, setImageUrls] = useState(['', '', '']);

    const fetchUser = async () => {
        let userInfo = await fetch('http://localhost:5000/me', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('3tography-access-token')}`
            }
        });
        userInfo = await userInfo.json();
        setUsername(userInfo.user);
        setImageUrls(userInfo.imageUrls);
    }

    useEffect(() => {
        fetchUser();
    }, [])

    return (
        <div class='container'>
            <div class='heading'>
                <div class='profile-wrapper'>
                    <img id='profile' src={imageUrls[0]}/>
                </div>
                <h2>{username}</h2>
                <p>UW '25 Dreamer ; Traveller; Explorer</p>
            </div>
            <div class='row'>
                <div class='col-lg-4 col-sm-12'>
                    <Image url={imageUrls[0]} pos='one' refresh={fetchUser}></Image>
                </div>
                <div class='col-lg-4 col-sm-12'>
                    <Image url={imageUrls[1]} pos='two' refresh={fetchUser}></Image>
                </div>
                <div class='col-lg-4 col-sm-12'>
                    <Image url={imageUrls[2]} pos='three' refresh={fetchUser}></Image>
                </div>
            </div>
        </div>
    )
}

export default User;