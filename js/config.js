const CONFIG = {
    highlightDuration: 5000, // Duration in milliseconds
    suitOrder: ['Spades', 'Hearts', 'Clubs', 'Diamonds'],
    rankDisplayOrder: ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
    rankRunOrderAceLow: ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
    rankRunOrderAceHigh: ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
    roundWhenCardPlayingIsEnabled: 2, // Round when cards may be played
    cardsDealt: 7, // Number of cards dealt to each player
    points: {
        A: 15,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        J: 10,
        Q: 10,
        K: 10
    },
    aceUsage: 'both' // Options: 'low', 'high', 'both'
};
