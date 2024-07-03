Game.prototype.drawFromStock = function() {
    if (this.hasDrawnCard) {
        alert('You can only draw once per turn.');
        return;
    }
    if (this.deck.cards.length === 0) {
        alert('The deck is empty.');
        return;
    }

    const card = this.deck.draw();
    this.getCurrentPlayer().hand.addCard(card);
    this.hasDrawnCard = true;
    this.drawnCard = card; // Store the drawn card reference
    this.renderHands();
    this.highlightDrawnCard();
    this.checkButtons();
};

Game.prototype.drawFromDiscardPile = function() {
    if (this.hasDrawnCard) {
        alert('You can only draw once per turn.');
        return;
    }
    if (this.discardPile.cards.length === 0) {
        alert('The discard pile is empty.');
        return;
    }

    const card = this.discardPile.cards.pop();
    this.getCurrentPlayer().hand.addCard(card);
    this.hasDrawnCard = true;
    this.drawnCard = card; // Store the drawn card reference
    this.renderHands();
    this.renderDiscardPile();
    this.highlightDrawnCard();
    this.checkButtons();
};

Game.prototype.highlightDrawnCard = function() {
    const handElement = document.getElementById(`hand${this.currentPlayerIndex + 1}`);
    Array.from(handElement.children).forEach((cardElement, index) => {
        const cardData = this.getCurrentPlayer().hand.cards[index];
        if (cardData === this.drawnCard) {
            cardElement.classList.add('highlight');
            setTimeout(() => {
                cardElement.classList.remove('highlight');
            }, CONFIG.highlightDuration); // Use the duration from the config file
        }
    });
};
