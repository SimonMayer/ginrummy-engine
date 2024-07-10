import apiService from './apiService';
import cardsService from './cardsService';

const turnsService = {
    async drawFromStockPile(matchId) {
        const turnData = await apiService.post(`/matches/${matchId}/actions/draw_from_stock_pile`, {}, 'Failed to draw from stock pile!');
        return await cardsService.getCard(turnData.card_id);
    },
    async discardCard(matchId, cardId) {
        await apiService.post(`/matches/${matchId}/actions/discard_card`, { card_id: cardId }, 'Failed to discard card!');
    }
};

export default turnsService;
