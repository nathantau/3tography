import React, { useEffect, useState } from 'react';
import './styles/Feed.css'
import FeedUtils from '../utils/feed';

const Feed = () => {

    const [following, setFollowing] = useState([]);

    useEffect(async () => {
        const res = await FeedUtils.getFollowing();
        if (res) {
            setFollowing(res);
        }
    }, []);

    return (
        <>
            {following.map(user => {
                return (
                    <div className='card' key={user.user}>
                        <h1>{user.user}</h1>
                        <div class='row' key={user.user}>
                            <div class='col-lg-4 col-sm-12'>
                                <div className='feed-image-wrapper'>
                                    <img src={user.imageUrls[0]}></img>
                                </div>
                            </div>
                            <div class='col-lg-4 col-sm-12'>
                                <div className='feed-image-wrapper'>
                                    <img src={user.imageUrls[1]}></img>
                                </div>                           
                            </div>
                            <div class='col-lg-4 col-sm-12'>
                                <div className='feed-image-wrapper'>
                                    <img src={user.imageUrls[2]}></img>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            })}
        </>
    );
}

export default Feed;