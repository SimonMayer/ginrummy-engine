class Game {
    constructor() {
        this.deck = new Deck();
        this.players = [new Player(1), new Player(2)];
        this.discardPile = new DiscardPile();
        this.currentPlayerIndex = 0;
        this.round = 1; // Initialize the round count
        this.selectedCards = [];
        this.hasDrawnCard = false;
        this.drawnCard = null; // Store reference to drawn card
        this.initialize();
    }

    initialize() {
        this.deck.shuffle();
        this.dealCards();
        this.renderHands();
        this.renderDiscardPile();
        this.checkButtons();
        this.updateScores();
    }

    dealCards() {
        this.players.forEach(player => {
            for (let i = 0; i < CONFIG.cardsDealt; i++) {
                player.hand.addCard(this.deck.draw());
            }
        });
    }

    switchTurn() {
        this.currentPlayerIndex = (this.currentPlayerIndex + 1) % this.players.length;
        this.hasDrawnCard = false;
        this.selectedCards = [];
        this.drawnCard = null; // Reset the drawn card reference

        if (this.currentPlayerIndex === 0) {
            this.round++; // Increment the round count when all players have had their turn
        }

        this.renderHands();
        this.checkButtons();
    }

    checkButtons() {
        const selectedCards = this.getSelectedCards();

        const enoughCardsSelectedForSet = selectedCards.length >= 3 && selectedCards.length <= 4;
        const allSameRank = selectedCards.every(card => card.rank === selectedCards[0]?.rank);
        const canPlaySet = enoughCardsSelectedForSet && allSameRank;

        const enoughCardsSelectedForRun = selectedCards.length >= 3;
        const allSameSuit = selectedCards.every(card => card.suit === selectedCards[0]?.suit);
        const canPlayRun = enoughCardsSelectedForRun && allSameSuit && isValidRun(selectedCards);

        const canDiscard = this.selectedCards.length === 1;

        const playSetButton = document.getElementById('playSetButton');
        const playRunButton = document.getElementById('playRunButton');
        const discardButton = document.getElementById('discardButton');
        const drawButton = document.getElementById('drawButton');
        const takeFromDiscardPileButton = document.getElementById('takeFromDiscardPileButton');

        playSetButton.disabled = !canPlaySet || this.round < CONFIG.roundWhenCardPlayingIsEnabled; // Disable play set button until the specified round
        playRunButton.disabled = !canPlayRun || this.round < CONFIG.roundWhenCardPlayingIsEnabled; // Disable play run button until the specified round
        discardButton.disabled = !canDiscard;

        // Disable draw buttons if a card has been drawn already
        drawButton.disabled = this.hasDrawnCard || this.deck.cards.length === 0;
        takeFromDiscardPileButton.disabled = this.hasDrawnCard || this.discardPile.cards.length === 0;
    }

    updateScores() {
        this.players.forEach((player, playerIndex) => {
            document.getElementById(`score${playerIndex + 1}`).innerText = `Score: ${player.score}`;
        });
    }

    discardCard() {
        if (!this.hasDrawnCard) {
            alert('You must draw a card before discarding.');
            return;
        }
        if (this.selectedCards.length !== 1) {
            alert('You must select exactly one card to discard.');
            return;
        }

        const [playerIndex, cardIndex] = this.selectedCards[0].split('-').map(Number);
        const card = this.getCurrentPlayer().hand.removeCard(cardIndex);
        this.discardPile.addCard(card);
        this.selectedCards = [];
        this.hasDrawnCard = false;
        this.switchTurn();
        this.renderHands();
        this.renderDiscardPile();
        this.checkButtons();
    }

    getCurrentPlayer() {
        return this.players[this.currentPlayerIndex];
    }
}
