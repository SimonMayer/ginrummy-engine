<template>
  <div class="visible-card">
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
import { getSuitEmoji, getDisplayRank, getSuitRepeat } from '../utils/cardUtils';

export default {
  name: 'VisibleCard',
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
      return getSuitEmoji(this.card.suit);
    },
    displayRank() {
      return getDisplayRank(this.card.rank);
    },
    suitRepeat() {
      return getSuitRepeat(this.card.rank);
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
.visible-card {
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
