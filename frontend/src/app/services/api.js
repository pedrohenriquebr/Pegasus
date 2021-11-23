import axios from 'axios';

export default axios.create({
   
    baseURL: '/api',
    headers: {
        'Accept': '*/*',
        'Content-Type': 'application/json',
        "Access-Control-Allow-Origin": "*"
    },
    auth: {
        username: process.env.REACT_APP_USER,
        password: process.env.REACT_APP_PASSWORD
    },
});

