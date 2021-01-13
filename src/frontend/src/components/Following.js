import React from 'react';

const Following = props => {

    const imageUrls = props.imageUrls;
    const profileUrl = props.profileUrl;
    const username = props.username;

    return (
        <>
            <h1>{username}</h1>
            <img src={imageUrls[0]}></img>
            <img src={imageUrls[1]}></img>
            <img src={imageUrls[2]}></img>
        </>
    )
}

export default Following;