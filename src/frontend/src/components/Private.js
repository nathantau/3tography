import React, { useEffect, useState } from 'react';
import { Route, Redirect } from 'react-router-dom';

const PrivateRoute = ({ component: Component, authenticated, ...rest }) => {
    return (
        <Route {...rest} render={() => (
            authenticated ?
                <Component/>
                : <Redirect to="/login" />
        )} />
    );
};

export default PrivateRoute;