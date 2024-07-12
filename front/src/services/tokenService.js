import axios from 'axios';

const BASE_URL = process.env.VUE_APP_BASE_URL;

// Create an axios instance for token refresh requests
const refreshClient = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

async function refreshSseToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
        throw new Error('Refresh token not found in local storage');
    }
    try {
        const response = await refreshClient.post('/auth/refresh/sse', {}, {
            headers: { 'Authorization': `Bearer ${refreshToken}` }
        });
        const newSseAccessToken = response.data.sse_access_token;
        localStorage.setItem('sse_access_token', newSseAccessToken);
        return newSseAccessToken;
    } catch (error) {
        localStorage.removeItem('rest_access_token');
        localStorage.removeItem('sse_access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/'; // Redirect to login
        throw error;
    }
}

export { refreshSseToken };
