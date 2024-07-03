class DiscardPile {
    constructor() {
        this.cards = [];
    }

    addCard(card) {
        this.cards.push(card);
    }

    takeTopCard() {
        if (this.cards.length > 0) {
            return this.cards.pop();
        } else {
            return null; // Or handle empty discard pile scenario
        }
    }

    peekTopCard() {
        if (this.cards.length > 0) {
            return this.cards[this.cards.length - 1];
        } else {
            return null; // Or handle empty discard pile scenario
        }
    }

    display(elementId) {
        const discardPileElement = document.getElementById(elementId);
        discardPileElement.innerHTML = '';
        this.cards.forEach((card, index) => {
            const cardElement = document.createElement('div');
            cardElement.className = 'card';
            cardElement.innerHTML = card.toString();
            cardElement.style.position = 'absolute';
            cardElement.style.left = `${index * 30}px`; // Adjust this value to control overlap
            discardPileElement.appendChild(cardElement);
        });
    }
}
