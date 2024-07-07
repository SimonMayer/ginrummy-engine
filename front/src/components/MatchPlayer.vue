<template>
  <li :class="['player-item', { 'current-turn': isCurrentTurn }]">
    {{ player.username }}
    <ul class="hand" v-if="!isSignedInUser">
      <li v-for="n in player.handSize" :key="n" class="card-item">
        <HiddenCard />
      </li>
    </ul>
    <ul class="hand" v-else>
      <li v-for="card in myHand" :key="card.card_id" class="card-item">
        <VisibleCard :cardProp="card" />
      </li>
    </ul>
  </li>
</template>

<script>
import HiddenCard from './HiddenCard.vue';
import VisibleCard from './VisibleCard.vue';

export default {
  name: 'MatchPlayer',
  components: {
    HiddenCard,
    VisibleCard
  },
  props: {
    player: {
      type: Object,
      required: true
    },
    myHand: {
      type: Array,
      required: true
    },
    signedInUserId: {
      type: Number,
      required: true
    },
    currentTurnUserId: {
      type: [Number, null],
      required: true
    }
  },
  computed: {
    isSignedInUser() {
      return this.player.user_id === this.signedInUserId;
    },
    isCurrentTurn() {
      return this.player.user_id === this.currentTurnUserId;
    }
  }
};
</script>

<style scoped>
.player-item {
  background-color: #f9f9f9;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ddd;
}

.current-turn {
  border: 2px solid #4CAF50;
  background-color: #e8f5e9;
}

.hand {
  display: flex;
  flex-direction: row;
  padding: 0;
  margin: 10px 0 0 0;
  list-style-type: none;
}

.card-item:not(:first-child) {
  margin-left: -80px;
}
</style>
