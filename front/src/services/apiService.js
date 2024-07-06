// services/apiService.js

import apiClient from '../api/axios';

const apiService = {
    async get(endpoint, errorMessage) {
        try {
            const response = await apiClient.get(endpoint);
            return response.data;
        } catch (error) {
            console.error(errorMessage, error);
            throw new Error(errorMessage);
        }
    },
    async post(endpoint, data, errorMessage) {
        try {
            const response = await apiClient.post(endpoint, data);
            return response.data;
        } catch (error) {
            console.error(errorMessage, error);
            throw new Error(errorMessage);
        }
    }
};

export default apiService;
