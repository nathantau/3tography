import React from 'react';
import './styles/Card.css'

const Login = () => {

    return (
        <>
            <div className='card'>
                <h1>Register</h1>
                <form>
                    <input type='text' placeholder='Please enter your username'></input>
                    <input type='password' placeholder='Please enter your password'></input>
                    <input type='submit' value='Register'></input>
                </form>
                <p>Already have an account? Login here</p>
            </div>
        </>
    )
}

export default Login;
