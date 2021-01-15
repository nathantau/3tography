import React, { useEffect } from 'react';
import { Route, Redirect } from 'react-router-dom';
import Auth from '../utils/auth';

const PrivateRoute = ({ component: Component, authenticated, ...rest }) => {
    console.log('yo', Auth.authenticated)
    return (
        <Route {...rest} render={() => (
            Auth.authenticated ?
                <Component/>
                : <Redirect to="/register" />
        )} />
    );
};

export default PrivateRoute;