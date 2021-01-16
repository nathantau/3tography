import React, { useEffect, useState } from 'react';
import Image from './Image';
import './styles/User.css'

const User = () => {

    const [username, setUsername] = useState('');
    const [description, setDescription] = useState('');
    const [imageUrls, setImageUrls] = useState(['', '', '']);

    const fetchUser = async () => {
        try {
            let userInfo = await fetch('http://localhost:5000/me', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('3tography-access-token')}`
                }
            });
            userInfo = await userInfo.json();
            if (userInfo) {
                setUsername(userInfo.user);
                setDescription(userInfo.description);
                setImageUrls(userInfo.imageUrls);
            }
        } catch (err) {
            console.error(err);
        }
    }

    useEffect(() => {
        fetchUser();
    }, [])

    return (
        <>
        {
            imageUrls && imageUrls.length === 3 ?
                <div class='container'>
                    <div class='heading'>
                        <div class='profile-wrapper'>
                            <img id='profile' src={imageUrls[0]}/>
                        </div>
                        <h2>{username}</h2>
                        <p>{description}</p>
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
            :
            null
        }
        </>
    )
}

export default User;