<template>
  <ul class="players-list">
    <MatchPlayer
        v-for="player in players"
        :key="player.user_id"
        :username="player.username"
        :hand="player.user_id === signedInUserId ? myHand : []"
        :hiddenCardCount="player.user_id !== signedInUserId ? player.handSize : 0"
        :highlightPlayer="player.user_id === currentTurnUserId"
        :selectable="isCurrentUserTurn"
    />
  </ul>
</template>

<script>
import MatchPlayer from './MatchPlayer.vue';

export default {
  name: 'MatchPlayerList',
  components: {
    MatchPlayer,
  },
  props: {
    players: {
      type: Array,
      required: true,
    },
    myHand: {
      type: Array,
      required: true,
    },
    signedInUserId: {
      type: Number,
      required: true,
    },
    currentTurnUserId: {
      type: [Number, null],
      required: true,
    },
  },
  computed: {
    isCurrentUserTurn() {
      return this.currentTurnUserId === this.signedInUserId;
    }
  }
};
</script>

<style scoped>
.players-list {
  list-style-type: none;
  padding: 0;
  width: 100%;
}
</style>
