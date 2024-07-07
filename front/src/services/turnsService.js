import apiService from './apiService';
import cardsService from './cardsService';

const turnsService = {
    async drawFromStockPile(turnId) {
        const turnData = await apiService.post(`/turns/${turnId}/draw_from_stock_pile`, {}, 'Failed to draw from stock pile!');
        return await cardsService.getCard(turnData.card_id);
    }
};

export default turnsService;
