import React, { useEffect } from 'react';
import { Route, Redirect } from 'react-router-dom';
import Auth from '../utils/auth';

const PrivateRoute = ({ component: Component, authenticated, ...rest }) => {
    return (
        <Route {...rest} render={() => (
            Auth.authenticated ?
                <Component/>
                : <Redirect to="/login" />
        )} />
    );
};

export default PrivateRoute;