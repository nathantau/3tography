import './App.css';

import { BrowserRouter as Router, Route } from 'react-router-dom';

import Me from './components/Me';
import Login from './components/Login';
import Register from './components/Register';
import PrivateRoute from './components/Private';
import Feed from './components/Feed';
import Auth from './utils/auth';
import Logo from './components/Logo';

function App() {

    Auth.init();

    return (
        <div className="App">
            <Router>
                <Logo></Logo>
                <PrivateRoute exact path='/' component={Me}></PrivateRoute>
                <PrivateRoute path='/feed' component={Feed}></PrivateRoute>
                <Route path='/register' component={Register}></Route>
                <Route path='/login' component={Login}></Route>
            </Router>
        </div>
    );
}

export default App;
