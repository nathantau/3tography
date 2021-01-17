import React from 'react';
import { useHistory } from 'react-router';
import { Link } from 'react-router-dom';
import Auth from '../utils/auth';


const Footer = () => {

    const history = useHistory();

    return (
        <footer className='fixed-bottom' style={{ backgroundColor: 'black', color: 'white', padding: '1vh', fontFamily: 'Roboto', fontWeight: 400 }}>
            <div className='row'>
                <div className='col-lg-1'></div>
                <div className='col-lg-2'>
                    <Link style={{ textDecoration: 'none', color: 'white' }} to={'/'}>
                        Me 📷
                    </Link>
                </div>
                <div className='col-lg-2'>
                    <Link style={{ textDecoration: 'none', color: 'white' }} to={'/feed'}>
                        Feed 🗞️
                    </Link>
                </div>
                <div className='col-lg-2'>
                    <Link style={{ textDecoration: 'none', color: 'white' }} to={'/search'}>
                        Follow 🔍
                    </Link>
                </div>
                <div className='col-lg-2'>
                    <Link style={{ textDecoration: 'none', color: 'white' }} onClick={() => Auth.logout(history)}>
                        Logout 🔒
                    </Link>
                </div>
                <div className='col-lg-2'>
                    <Link style={{ textDecoration: 'none', color: 'white' }} to={'/settings'}>
                        Settings ⚙️
                    </Link>
                </div>
            </div>
        </footer>

    )
}

export default Footer;
