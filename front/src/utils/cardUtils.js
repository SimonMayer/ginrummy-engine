export const suitEmojis = {
    Hearts: '♥️',
    Diamonds: '♦️',
    Clubs: '♣️',
    Spades: '♠️',
};

export const faceCards = {
    J: 'J',
    Q: 'Q',
    K: 'K',
    A: 'A',
};

export function getSuitEmoji(suit) {
    return suitEmojis[suit];
}

export function getDisplayRank(rank) {
    return faceCards[rank] || rank;
}

export function getSuitRepeat(rank) {
    return faceCards[rank] ? 1 : parseInt(rank, 10);
}
