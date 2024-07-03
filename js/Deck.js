class Deck {
    constructor() {
        this.cards = this.generateDeck();
        this.shuffle(); // Ensure the deck is shuffled upon initialization
    }

    generateDeck() {
        const ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
        const suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs'];
        let deck = [];
        for (let suit of suits) {
            for (let rank of ranks) {
                deck.push(new Card(rank, suit));
            }
        }
        return deck;
    }

    shuffle() {
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]]; // Swap
        }
    }

    draw() {
        return this.cards.pop();
    }
}
