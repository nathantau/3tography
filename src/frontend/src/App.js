import './App.css';

import { BrowserRouter as Router, Route, useHistory } from 'react-router-dom';

import Me from './components/Me';
import Login from './components/Login';
import Register from './components/Register';
import PrivateRoute from './components/Private';
import Auth from './utils/auth';
import { useEffect, useState } from 'react';

function App() {

    // const history = useHistory();
    // // Determine authorization status
    // useEffect(async () => {
    //     await Auth.init();
    //     if (!Auth.authenticated) {
    //         history.push('/login');
    //     } else {
    //     }
    // }, []);

    return (
        <div className="App">
            <div class='home-banner'>
                <h1>3tography</h1>
            </div>
            <Router>
                <Route exact path='/' component={Me}></Route>
                <PrivateRoute path='/feed' component={Me} authenticated={localStorage.getItem('3tography-access-token')}></PrivateRoute>
                <PrivateRoute path='/me' component={Me} authenticated={localStorage.getItem('3tography-access-token')}></PrivateRoute>
                <Route path='/register' component={Register}></Route>
                <Route path='/login' component={Login}></Route>
            </Router>
        </div>
    );
}

export default App;
