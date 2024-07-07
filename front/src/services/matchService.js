import apiService from './apiService';

const matchService = {
    async getMatchDetails(matchId) {
        return await apiService.get(`/matches/${matchId}`, 'Failed to fetch match details!');
    },
    async getPlayers(matchId) {
        return await apiService.get(`/matches/${matchId}/players`, 'Failed to fetch players!');
    },
    async getHandsForPlayers(roundId) {
        return await apiService.get(`/rounds/${roundId}`, 'Failed to fetch hands!');
    },
    async getMyHand(roundId) {
        return await apiService.get(`/rounds/${roundId}/my_hand`, 'Failed to fetch your hand!');
    },
    async getCurrentTurn(roundId) {
        return await apiService.get(`/rounds/${roundId}/current_turn`, 'Failed to fetch current turn!');
    },
    async drawFromStockPile(turnId) {
        const turnData = await apiService.post(`/turns/${turnId}/draw_from_stock_pile`, {}, 'Failed to draw from stock pile!');
        const cardData = await apiService.get(`/cards/${turnData.card_id}`, 'Failed to fetch card details!');
        return { new_card: cardData };
    },
    async startMatch(matchId) {
        return await apiService.post(`/matches/${matchId}/start`, {}, 'Failed to start match!');
    }
};

export default matchService;
