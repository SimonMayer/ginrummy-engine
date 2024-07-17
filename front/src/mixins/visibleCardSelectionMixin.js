export default {
    data() {
        return {
            selectedCards: []
        };
    },
    methods: {
        getSelectedCards() {
            if (!this.$refs.visibleCards) {
                return [];
            }
            return this.$refs.visibleCards.filter(visibleCard => visibleCard.isCardSelected());
        },
        handleSelected() {
            this.selectedCards = this.getSelectedCards().map(card => card.cardProp.card_id);
            this.$emit('update:selected');
        },
        unselectAllCards() {
            if (!this.$refs.visibleCards) {
                return;
            }
            this.$refs.visibleCards.forEach(visibleCard => visibleCard.unselect());
        },
        isSelected(card) {
            return this.selectedCards.includes(card.card_id);
        }
    }
};
