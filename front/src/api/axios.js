import axios from 'axios';

// Create an axios instance
const apiClient = axios.create({
    baseURL: 'http://localhost:5000', // Your API base URL
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add a request interceptor to include the access token in headers
apiClient.interceptors.request.use(config => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        config.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// Add a response interceptor to handle token refresh
apiClient.interceptors.response.use(response => {
    return response;
}, async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
            try {
                const response = await axios.post('http://localhost:5000/refresh', {}, {
                    headers: { 'Authorization': `Bearer ${refreshToken}` }
                });
                const newAccessToken = response.data.access_token;
                localStorage.setItem('access_token', newAccessToken);
                axios.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
                originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
                return axios(originalRequest);
            } catch (refreshError) {
                // If the refresh fails, clear both tokens and redirect to login
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/'; // Redirect to login
            }
        } else {
            window.location.href = '/'; // Redirect to login
        }
    }
    return Promise.reject(error);
});

export default apiClient;
