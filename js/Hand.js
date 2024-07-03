class Hand {
    constructor() {
        this.cards = [];
    }

    addCard(card) {
        this.cards.push(card);
    }

    removeCard(cardIndex) {
        return this.cards.splice(cardIndex, 1)[0];
    }
}
