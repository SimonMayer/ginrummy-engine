import apiService from './apiService';
import cardsService from './cardsService';

const turnsService = {
    async drawFromStockPile(turnId) {
        const turnData = await apiService.post(`/turns/${turnId}/draw_from_stock_pile`, {}, 'Failed to draw from stock pile!');
        const cardData = await cardsService.getCard(turnData.card_id);
        return { new_card: cardData };
    }
};

export default turnsService;
