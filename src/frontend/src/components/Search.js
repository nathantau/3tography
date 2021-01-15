import React, { useEffect, useState } from 'react';
import { useHistory, Link } from 'react-router-dom';
import './styles/Card.css';
import Auth from '../utils/auth';
import FeedUtils from '../utils/feed';

const server = 'http://localhost:5000';

const Search = () => {

    const history = useHistory();
    const [username, setUsername] = useState('');
    const [candidates, setCandidates] = useState([]);
    const [followingList, setFollowing] = useState(new Set());

    const handleSubmit = async event => {
        event.preventDefault();
        try {
            if (!username) {
                return;
            }
            const res = await fetch(`${server}/search?user=${username}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('3tography-access-token')}`
                }
            })
                .then(res => res.json());
            console.log(res);
            if (res.results) {
                setCandidates(res.results);
            }
        } catch (err) {
            console.error(err);
        }
    }

    const follow = async toFollow => {
        try {
            const res = await fetch(`${server}/follow`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('3tography-access-token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user: toFollow
                })
            }).then(res => res.json());
            if (res.followed) {
                setFollowing(new Set(followingList.add(toFollow)));
            }
        } catch (err) {
            console.error(err);
        }
    }

    const unfollow = async toUnfollow => {
        try {
            const res = await fetch(`${server}/unfollow`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('3tography-access-token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user: toUnfollow
                })
            }).then(res => res.json());
            if (res.unfollowed) {
                const updatedList = new Set(followingList);
                updatedList.delete(toUnfollow);
                setFollowing(new Set(updatedList));
            }
        } catch (err) {
            console.error(err);
        }
    }

    useEffect(() => {
        const fetchData = async () => {
            if (!await Auth.isLoggedIn()) {
                history.push('/login');
            }
            const following = await FeedUtils.getFollowing();
            if (following) {
                setFollowing(new Set(following.map(user => user.user)));
                console.log(followingList)
            }
        }
        fetchData();
    }, []);

    return (
        <>
            <div className='container'>
                <div className='prompt-card card'>
                    <h1>Search</h1>
                    <form onSubmit={handleSubmit} >
                        <input type='text' onChange={event => setUsername(event.target.value)} placeholder='Please enter a username'></input>
                        <input type='submit' value='Search'></input>
                    </form>
                    <div className='candidates' style={{ textAlign: 'left', margin: '25px 0' }}>
                        {
                            candidates.map(candidate => {
                                if (followingList.has(candidate)) {
                                    return (
                                        <p key={candidate}>
                                            <span style={{ fontWeight: 'bold' }}>{candidate}</span> <span style={{ color: 'green' }} onClick={() => unfollow(candidate)}>-following</span>
                                        </p>
                                    )
                                } else {
                                    return (
                                        <p key={candidate}>
                                            <span style={{ fontWeight: 'bold' }}>{candidate}</span> <span style={{ color: 'blue' }} onClick={() => follow(candidate)}>+follow</span>
                                        </p>
                                    )
                                }
                            })
                        }
                    </div>
                </div>
            </div>
        </>
    )
}

export default Search;
