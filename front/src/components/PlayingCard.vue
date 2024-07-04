<template>
  <div class="playing-card">
    <div :class="['card-content', rankClass, suitClass]">
      <CardCorner class="top-left" :rank="displayRank" :suit="suitEmoji" />
      <CardPattern :suitEmoji="suitEmoji" :suitRepeat="suitRepeat" />
      <CardCorner class="bottom-right" :rank="displayRank" :suit="suitEmoji" />
    </div>
  </div>
</template>

<script>
import CardCorner from './CardCorner.vue';
import CardPattern from './CardPattern.vue';

export default {
  name: 'PlayingCard',
  components: {
    CardCorner,
    CardPattern,
  },
  props: {
    card: {
      type: Object,
      required: true,
    },
  },
  computed: {
    suitEmoji() {
      const suitEmojis = {
        Hearts: '♥️',
        Diamonds: '♦️',
        Clubs: '♣️',
        Spades: '♠️',
      };
      return suitEmojis[this.card.suit];
    },
    displayRank() {
      const faceCards = {
        J: 'J',
        Q: 'Q',
        K: 'K',
        A: 'A',
      };
      return faceCards[this.card.rank] || this.card.rank;
    },
    suitRepeat() {
      const faceCards = {
        J: 1,
        Q: 1,
        K: 1,
        A: 1,
      };
      return faceCards[this.card.rank] || parseInt(this.card.rank, 10);
    },
    rankClass() {
      return `rank-${this.card.rank}`;
    },
    suitClass() {
      return this.card.suit.toLowerCase();
    },
  },
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

.top-left {
  top: 4px;
  left: 0px;
}

.bottom-right {
  bottom: 4px;
  right: 0px;
  transform: rotate(180deg);
}

.hearts, .diamonds {
  color: red;
}

.clubs, .spades {
  color: black;
}

/* Specific placement of each suit icon, for each rank */

/* rank 2 */
.card-content.rank-2 .suit-symbol:nth-child(1) {
  grid-column: 2;
  grid-row: 1 / span 4;
}

.card-content.rank-2 .suit-symbol:nth-child(2) {
  grid-column: 2;
  grid-row: 13 / span 4;
}

/* rank 3 */
.card-content.rank-3 .suit-symbol:nth-child(1) {
  grid-column: 2;
  grid-row: 1 / span 4;
}

.card-content.rank-3 .suit-symbol:nth-child(2) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

.card-content.rank-3 .suit-symbol:nth-child(3) {
  grid-column: 2;
  grid-row: 13 / span 4;
}

/* rank 4 */
.card-content.rank-4 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-4 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-4 .suit-symbol:nth-child(3) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-4 .suit-symbol:nth-child(4) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 5 */
.card-content.rank-5 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-5 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-5 .suit-symbol:nth-child(3) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

.card-content.rank-5 .suit-symbol:nth-child(4) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-5 .suit-symbol:nth-child(5) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 6 */
.card-content.rank-6 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-6 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-6 .suit-symbol:nth-child(3) {
  grid-column: 1;
  grid-row: 7 / span 4;
}

.card-content.rank-6 .suit-symbol:nth-child(4) {
  grid-column: 3;
  grid-row: 7 / span 4;
}

.card-content.rank-6 .suit-symbol:nth-child(5) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-6 .suit-symbol:nth-child(6) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 7 */
.card-content.rank-7 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(3) {
  grid-column: 2;
  grid-row: 4 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(4) {
  grid-column: 1;
  grid-row: 7 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(5) {
  grid-column: 3;
  grid-row: 7 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(6) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(7) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 8 */
.card-content.rank-8 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(3) {
  grid-column: 2;
  grid-row: 4 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(4) {
  grid-column: 1;
  grid-row: 7 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(5) {
  grid-column: 3;
  grid-row: 7 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(6) {
  grid-column: 2;
  grid-row: 10 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(7) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(8) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 9 */
.card-content.rank-9 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(3) {
  grid-column: 1;
  grid-row: 5 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(4) {
  grid-column: 3;
  grid-row: 5 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(5) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(6) {
  grid-column: 1;
  grid-row: 9 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(7) {
  grid-column: 3;
  grid-row: 9 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(8) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(9) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 10 */
.card-content.rank-10 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(3) {
  grid-column: 2;
  grid-row: 3 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(4) {
  grid-column: 1;
  grid-row: 5 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(5) {
  grid-column: 3;
  grid-row: 5 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(6) {
  grid-column: 1;
  grid-row: 9 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(7) {
  grid-column: 2;
  grid-row: 11 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(8) {
  grid-column: 3;
  grid-row: 9 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(9) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(10) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* non-numeric cards */
.card-content.rank-A .suit-symbol:nth-child(1),
.card-content.rank-J .suit-symbol:nth-child(1),
.card-content.rank-Q .suit-symbol:nth-child(1),
.card-content.rank-K .suit-symbol:nth-child(1) {
  grid-column: 2;
  grid-row: 7 / span 4;
}
</style>
