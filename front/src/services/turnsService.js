import apiService from '@/services/apiService';
import cardsService from '@/services/cardsService';

const turnsService = {
    async drawFromStockPile(matchId) {
        const turnData = await apiService.post(`/matches/${matchId}/actions/draw_from_stock_pile`, {}, 'Failed to draw from stock pile!');
        return await cardsService.getCard(turnData.card_id);
    },
    async drawFromEmptyStockPile(matchId) {
        const turnData = await apiService.post(`/matches/${matchId}/actions/draw_from_empty_stock_pile`, {}, 'Failed to draw from empty stock pile!');
        return await cardsService.getCard(turnData.card_id);
    },
    async drawFromDiscardPile(matchId) {
        const turnData = await apiService.post(`/matches/${matchId}/actions/draw_one_from_discard_pile`, {}, 'Failed to draw from discard pile!');
        return await cardsService.getCard(turnData.card_id);
    },
    async discardCard(matchId, cardId) {
        await apiService.post(`/matches/${matchId}/actions/discard_card`, { card_id: cardId }, 'Failed to discard card!');
    },
    async playMeld(matchId, cardIds, meldType) {
        await apiService.post(`/matches/${matchId}/actions/play_meld/${meldType}`, { card_ids: cardIds }, 'Failed to play meld!');
    },
    async extendMeld(matchId, meldId, cardIds) {
        await apiService.post(`/matches/${matchId}/actions/extend_meld/${meldId}`, { card_ids: cardIds }, 'Failed to extend meld!');
    }
};

export default turnsService;
