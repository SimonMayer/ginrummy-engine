import apiService from './apiService';

const matchesService = {
    async getMatchDetails(matchId) {
        return await apiService.get(`/matches/${matchId}`, 'Failed to fetch match details!');
    },
    async getPlayers(matchId) {
        return await apiService.get(`/matches/${matchId}/players`, 'Failed to fetch players!');
    },
    async startMatch(matchId) {
        return await apiService.post(`/matches/${matchId}/start`, {}, 'Failed to start match!');
    }
};

export default matchesService;
