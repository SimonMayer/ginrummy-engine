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
</style>
