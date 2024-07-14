import apiService from '@/services/apiService';

const configService = {
    async getGameConfig() {
        return await apiService.get('/config/game', 'Failed to fetch game configuration!');
    }
};

export default configService;
