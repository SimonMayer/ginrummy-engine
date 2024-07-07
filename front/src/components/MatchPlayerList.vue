<template>
  <ul class="players-list">
    <MatchPlayer
        v-for="player in players"
        :key="player.user_id"
        :player="player"
        :myHand="myHand"
        :signedInUserId="signedInUserId"
        :currentTurnUserId="currentTurnUserId"
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
};
</script>

<style scoped>
.players-list {
  list-style-type: none;
  padding: 0;
  width: 100%;
}
</style>
