import React, { useEffect, useState } from 'react';
import './styles/Feed.css'
import './styles/Card.css'
import FeedUtils from '../utils/feed';
import Auth from '../utils/auth';
import { useHistory } from 'react-router';

const Feed = () => {

    const [following, setFollowing] = useState([]);

    const history = useHistory();

    useEffect(() => {
        const fetchData = async () => {
            if (!await Auth.isLoggedIn()) {
                history.push('/login');
            } else {
                const res = await FeedUtils.getFollowing();
                if (res) {
                    setFollowing(res);
                }
            }
        }
        fetchData();
    }, []);

    return (
        <>
            {following.map(user => {
                return (
                    <div className='card feed-card' key={user.user}>
                        <div class='feed-profile-wrapper'>
                            <img id='profile' src={user.imageUrls[0]}/>
                        </div>
                        <h2>{user.user}</h2>
                        {user.description ? <p>{user.description}</p> : null}
                        <div class='row' key={user.user}>
                            <div class='col-lg-4 col-sm-12'>
                                <div className='feed-image-wrapper'>
                                    <img alt='image0' src={user.imageUrls[0]}></img>
                                </div>
                            </div>
                            <div class='col-lg-4 col-sm-12'>
                                <div className='feed-image-wrapper'>
                                    <img alt='image1' src={user.imageUrls[1]}></img>
                                </div>                           
                            </div>
                            <div class='col-lg-4 col-sm-12'>
                                <div className='feed-image-wrapper'>
                                    <img alt='image2' src={user.imageUrls[2]}></img>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            })}
            <div className='container'></div>
        </>
    );
}

export default Feed;