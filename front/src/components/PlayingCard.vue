<template>
  <div class="playing-card">
    <div :class="['card-content', rankClass, suitClass]">
      <div class="corner top-left">
        <div>{{ displayRank }}</div>
        <div>{{ suitEmoji }}</div>
      </div>
      <div class="suits">
        <div v-for="n in suitRepeat" :key="n" class="suit-large">{{ suitEmoji }}</div>
      </div>
      <div class="corner bottom-right">
        <div>{{ displayRank }}</div>
        <div>{{ suitEmoji }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayingCard',
  props: {
    card: {
      type: Object,
      required: true
    }
  },
  computed: {
    suitEmoji() {
      const suitEmojis = {
        'Hearts': '♥️',
        'Diamonds': '♦️',
        'Clubs': '♣️',
        'Spades': '♠️'
      };
      return suitEmojis[this.card.suit];
    },
    displayRank() {
      const faceCards = {
        'J': 'J',
        'Q': 'Q',
        'K': 'K',
        'A': 'A'
      };
      return faceCards[this.card.rank] || this.card.rank;
    },
    suitRepeat() {
      const faceCards = {
        'J': 1,
        'Q': 1,
        'K': 1,
        'A': 1
      };
      return faceCards[this.card.rank] || parseInt(this.card.rank, 10);
    },
    rankClass() {
      return `rank-${this.card.rank}`;
    },
    suitClass() {
      return this.card.suit.toLowerCase();
    }
  }
};
</script>

<style scoped>
.playing-card {
  display: inline-block;
  margin: 10px;
}

.card-content {
  position: relative;
  width: 100px;
  height: 150px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: white;
  text-align: center;
}

.corner {
  position: absolute;
  width: 20px;
  font-size: 12px;
}

.top-left {
  top: 4px;
  left: 0px;
}

.bottom-right {
  bottom: 4px;
  right: 0px;
  transform: rotate(180deg);
}

.suits {
  position: absolute;
  top: 10px;
  bottom: 10px;
  left: 20px;
  right: 20px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(16, 1fr);
  justify-content: center;
  justify-items: center;
  align-items: center;
}

.suit-large {
  font-size: 20px;
}

.hearts {
  color: red;
}

.diamonds {
  color: red;
}

.clubs, .spades {
  color: black;
}

/* Specific placement of each suit icon, for each rank */
/* rank A */
.card-content.rank-A .suit-large:nth-child(1) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

/* rank 2 */
.card-content.rank-2 .suit-large:nth-child(1) {
  grid-column: 2;
  grid-row: 1 / span 4;
}

.card-content.rank-2 .suit-large:nth-child(2) {
  grid-column: 2;
  grid-row: 13 / span 4;
}

/* rank 3 */
.card-content.rank-3 .suit-large:nth-child(1) {
  grid-column: 2;
  grid-row: 1 / span 4;
}

.card-content.rank-3 .suit-large:nth-child(2) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

.card-content.rank-3 .suit-large:nth-child(3) {
  grid-column: 2;
  grid-row: 13 / span 4;
}

/* rank 4 */
.card-content.rank-4 .suit-large:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-4 .suit-large:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-4 .suit-large:nth-child(3) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-4 .suit-large:nth-child(4) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 5 */
.card-content.rank-5 .suit-large:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-5 .suit-large:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-5 .suit-large:nth-child(3) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

.card-content.rank-5 .suit-large:nth-child(4) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-5 .suit-large:nth-child(5) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 6 */
.card-content.rank-6 .suit-large:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-6 .suit-large:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-6 .suit-large:nth-child(3) {
  grid-column: 1;
  grid-row: 7 / span 4;
}

.card-content.rank-6 .suit-large:nth-child(4) {
  grid-column: 3;
  grid-row: 7 / span 4;
}

.card-content.rank-6 .suit-large:nth-child(5) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-6 .suit-large:nth-child(6) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 7 */
.card-content.rank-7 .suit-large:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-7 .suit-large:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-7 .suit-large:nth-child(3) {
  grid-column: 2;
  grid-row: 4 / span 4;
}

.card-content.rank-7 .suit-large:nth-child(4) {
  grid-column: 1;
  grid-row: 7 / span 4;
}

.card-content.rank-7 .suit-large:nth-child(5) {
  grid-column: 3;
  grid-row: 7 / span 4;
}

.card-content.rank-7 .suit-large:nth-child(6) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-7 .suit-large:nth-child(7) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 8 */
.card-content.rank-8 .suit-large:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-8 .suit-large:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-8 .suit-large:nth-child(3) {
  grid-column: 2;
  grid-row: 4 / span 4;
}

.card-content.rank-8 .suit-large:nth-child(4) {
  grid-column: 1;
  grid-row: 7 / span 4;
}

.card-content.rank-8 .suit-large:nth-child(5) {
  grid-column: 3;
  grid-row: 7 / span 4;
}

.card-content.rank-8 .suit-large:nth-child(6) {
  grid-column: 2;
  grid-row: 10 / span 4;
}

.card-content.rank-8 .suit-large:nth-child(7) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-8 .suit-large:nth-child(8) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 9 */
.card-content.rank-9 .suit-large:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-9 .suit-large:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-9 .suit-large:nth-child(3) {
  grid-column: 1;
  grid-row: 5 / span 4;
}

.card-content.rank-9 .suit-large:nth-child(4) {
  grid-column: 3;
  grid-row: 5 / span 4;
}

.card-content.rank-9 .suit-large:nth-child(5) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

.card-content.rank-9 .suit-large:nth-child(6) {
  grid-column: 1;
  grid-row: 9 / span 4;
}

.card-content.rank-9 .suit-large:nth-child(7) {
  grid-column: 3;
  grid-row: 9 / span 4;
}

.card-content.rank-9 .suit-large:nth-child(8) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-9 .suit-large:nth-child(9) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 10 */
.card-content.rank-10 .suit-large:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-10 .suit-large:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-10 .suit-large:nth-child(3) {
  grid-column: 2;
  grid-row: 3 / span 4;
}

.card-content.rank-10 .suit-large:nth-child(4) {
  grid-column: 1;
  grid-row: 5 / span 4;
}

.card-content.rank-10 .suit-large:nth-child(5) {
  grid-column: 3;
  grid-row: 5 / span 4;
}

.card-content.rank-10 .suit-large:nth-child(6) {
  grid-column: 1;
  grid-row: 9 / span 4;
}

.card-content.rank-10 .suit-large:nth-child(7) {
  grid-column: 2;
  grid-row: 11 / span 4;
}

.card-content.rank-10 .suit-large:nth-child(8) {
  grid-column: 3;
  grid-row: 9 / span 4;
}

.card-content.rank-10 .suit-large:nth-child(9) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-10 .suit-large:nth-child(10) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank J */
.card-content.rank-J .suit-large:nth-child(1) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

/* rank Q */
.card-content.rank-Q .suit-large:nth-child(1) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

/* rank K */
.card-content.rank-K .suit-large:nth-child(1) {
  grid-column: 2;
  grid-row: 7 / span 4;
}
</style>
