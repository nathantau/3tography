import React, { useEffect, useState } from 'react';
import Following from './Following';

const User = ({ username }) => {

    const [imageUrls, setImageUrls] = useState([]);

    useEffect(() => {
        const fetchUser = async () => {
            const userInfo = await fetch('http://localhost:5000/me', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user: 'sam'
                })
            }).then(res => res.json());
            console.log(userInfo)
            setImageUrls(userInfo.imageUrls);
        }
        fetchUser();
    }, [])

    return (
        <div>
            <h1>{username}</h1>
            <img src={imageUrls[0]}></img>
            <img src={imageUrls[1]}></img>
            <img src={imageUrls[2]}></img>
        </div>
    )
}

export default User;