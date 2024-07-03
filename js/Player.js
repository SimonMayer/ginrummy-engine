class Player {
    constructor(id) {
        this.id = id;
        this.hand = new Hand();
        this.sets = [];
        this.score = 0;
    }

    adjustScoreBy(points) {
        this.score += points;
    }
}
