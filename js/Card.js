class Card {
    constructor(rank, suit) {
        this.rank = rank;
        this.suit = suit;
    }

    toString() {
        const suitSymbols = {
            'Diamonds': '♦️',
            'Hearts': '♥️',
            'Spades': '♠️',
            'Clubs': '♣️'
        };
        const suitSymbol = suitSymbols[this.suit];
        let suitDisplay = '';

        switch (this.rank) {
            case 'A':
                suitDisplay += `<div class="suit-large">${suitSymbol}</div>`;
                break;
            case 'J':
            case 'Q':
            case 'K':
                suitDisplay += `<div class="suit-large">${this.rank}</div>`;
                break;
            default:
                for (let i = 0; i < parseInt(this.rank); i++) {
                    suitDisplay += `<div class="suit-large">${suitSymbol}</div>`;
                }
        }

        return `
            <div class="card-content rank-${this.rank} ${this.suit.toLowerCase()}">
                <div class="corner top-left">
                    <div>${this.rank}</div>
                    <div>${suitSymbol}</div>
                </div>
                <div class="suits">${suitDisplay}</div>
                <div class="corner bottom-right">
                    <div>${this.rank}</div>
                    <div>${suitSymbol}</div>
                </div>
            </div>
        `;
    }
}
