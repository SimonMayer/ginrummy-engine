<template>
  <ul class="players-list">
    <MatchPlayer
        v-for="player in players"
        :key="player.user_id"
        :username="player.username"
        :hand="player.hand"
        :hiddenCardCount="player.hiddenCardCount"
        :highlightPlayer="player.highlightPlayer"
        :selectable="player.selectable"
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
