import apiService from '@/services/apiService';

const cardsService = {
    async getCard(cardId) {
        return await apiService.get(`/cards/${cardId}`, 'Failed to fetch card details!');
    }
};

export default cardsService;
