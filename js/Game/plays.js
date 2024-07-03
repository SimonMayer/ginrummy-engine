function areCardsOfConsecutiveRank(cards, rankRunOrder) {
    const ranks = cards.map(card => card.rank);
    let rankIndices = ranks.map(rank => rankRunOrder.indexOf(rank)).sort((a, b) => a - b);

    if (0 === rankIndices.length) {
        return false;
    }
    for (let i = 1; i < rankIndices.length; i++) {
        if (rankIndices[i] !== rankIndices[i - 1] + 1) {
            return false;
        }
    }

    return true;
}

function isValidRun(cards) {
    // Check that all cards are of the same suit
    const allSameSuit = cards.every(card => card.suit === cards[0].suit);
    if (!allSameSuit) {
        return false;
    }

    let isConsecutiveRankWithAceHigh = areCardsOfConsecutiveRank(cards, CONFIG.rankRunOrderAceHigh);
    let isConsecutiveRankWithAceLow = areCardsOfConsecutiveRank(cards, CONFIG.rankRunOrderAceLow);

    if (CONFIG.aceUsage === 'low' && !isConsecutiveRankWithAceLow) {
        return false;
    }

    if (CONFIG.aceUsage === 'high' && !isConsecutiveRankWithAceHigh) {
        return false;
    }

    if (CONFIG.aceUsage === 'both' && !(isConsecutiveRankWithAceLow || isConsecutiveRankWithAceHigh)) {
        return false;
    }

    return true;
}

Game.prototype.playSet = function() {
    if (this.round < CONFIG.roundWhenCardPlayingIsEnabled) {
        alert(`You cannot play a set until round ${CONFIG.roundWhenCardPlayingIsEnabled}.`);
        return;
    }

    const selectedCards = this.selectedCards.map(cardKey => {
        const [playerIndex, cardIndex] = cardKey.split('-').map(Number);
        return this.players[playerIndex].getCards()[cardIndex];
    });

    const playerIndex = this.currentPlayer;

    const player = this.players[playerIndex];
    const newHand = player.getCards().filter(card => !selectedCards.includes(card));
    const setCards = selectedCards.slice(0);

    this.players[playerIndex].hand.cards = newHand;
    this.players[playerIndex].sets.push(setCards);

    // Calculate and update score
    const points = setCards.reduce((total, card) => total + CONFIG.points[card.rank], 0);
    this.players[playerIndex].score += points;

    this.selectedCards = [];
    this.renderHands();
    this.renderSets();
    this.checkButtons();
    this.updateScores(); // Update the scores display
};

Game.prototype.playRun = function() {
    if (this.round < CONFIG.roundWhenCardPlayingIsEnabled) {
        alert(`You cannot play a run until round ${CONFIG.roundWhenCardPlayingIsEnabled}.`);
        return;
    }

    const selectedCards = this.selectedCards.map(cardKey => {
        const [playerIndex, cardIndex] = cardKey.split('-').map(Number);
        return this.players[playerIndex].getCards()[cardIndex];
    });

    const playerIndex = this.currentPlayer;
    const suit = selectedCards[0].suit;

    const player = this.players[playerIndex];
    const newHand = player.getCards().filter(card => card.suit !== suit || !selectedCards.includes(card));
    const runCards = selectedCards.slice(0);

    this.players[playerIndex].hand.cards = newHand;
    this.players[playerIndex].sets.push(runCards);

    // Calculate and update score
    const points = runCards.reduce((total, card) => total + CONFIG.points[card.rank], 0);
    this.players[playerIndex].score += points;

    this.selectedCards = [];
    this.renderHands();
    this.renderSets();
    this.checkButtons();
    this.updateScores(); // Update the scores display
};
