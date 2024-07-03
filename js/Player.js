class Player {
    constructor(id) {
        this.id = id;
        this.hand = new Hand();
        this.sets = [];
        this.score = 0;
    }

    addSet(cards) {
        this.sets.push(cards);
        this.updateScore(cards);
    }

    updateScore(cards) {
        this.score += cards.reduce((total, card) => total + CONFIG.points[card.rank], 0);
    }
}
