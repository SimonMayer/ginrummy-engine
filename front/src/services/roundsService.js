import apiService from './apiService';

const roundsService = {
    async getHandsForPlayers(roundId) {
        return await apiService.get(`/rounds/${roundId}`, 'Failed to fetch hands!');
    },
    async getMyHand(roundId) {
        return await apiService.get(`/rounds/${roundId}/my_hand`, 'Failed to fetch your hand!');
    },
    async getCurrentTurn(roundId) {
        return await apiService.get(`/rounds/${roundId}/current_turn`, 'Failed to fetch current turn!');
    }
};

export default roundsService;
