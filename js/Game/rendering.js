Game.prototype.renderHands = function() {
    this.players.forEach((player, playerIndex) => {
        const handElement = document.getElementById(`hand${playerIndex + 1}`);
        handElement.innerHTML = '';
        player.hand.cards.sort((a, b) => {
            if (a.suit === b.suit) {
                return CONFIG.rankDisplayOrder.indexOf(a.rank) - CONFIG.rankDisplayOrder.indexOf(b.rank);
            }
            return CONFIG.suitOrder.indexOf(a.suit) - CONFIG.suitOrder.indexOf(b.suit);
        }).forEach((card, cardIndex) => {
            const cardElement = document.createElement('div');
            cardElement.className = 'card';
            cardElement.id = `${playerIndex}-${cardIndex}`;
            cardElement.innerHTML = card.toString();
            cardElement.onclick = () => this.selectCard(playerIndex, cardIndex);
            handElement.appendChild(cardElement);
        });
    });

    document.getElementById('roundNumber').innerText = `Round: ${this.round}`;
};


Game.prototype.renderDiscardPile = function() {
    const discardPileElement = document.getElementById('discardPile');
    discardPileElement.innerHTML = '';

    this.discardPile.cards.forEach((card, index) => {
        const cardElement = document.createElement('div');
        cardElement.className = 'card';
        cardElement.style.setProperty('--i', index);
        cardElement.innerHTML = card.toString();
        discardPileElement.appendChild(cardElement);
    });
};

Game.prototype.renderSets = function() {
    this.players.forEach((player, playerIndex) => {
        const setsElement = document.getElementById(`sets${playerIndex + 1}`);
        setsElement.innerHTML = '';
        player.sets.forEach(set => {
            const setElement = document.createElement('div');
            setElement.className = 'set';
            set.forEach((card, cardIndex) => {
                const cardElement = document.createElement('div');
                cardElement.className = 'card';
                cardElement.style.setProperty('--i', cardIndex);
                cardElement.innerHTML = card.toString();
                setElement.appendChild(cardElement);
            });
            setsElement.appendChild(setElement);
        });
    });
};
