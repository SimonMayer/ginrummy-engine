<template>
  <div class="player-item non-self-player" :class="{ 'highlighted': highlightPlayer }">
    <div class="hand">
      <HiddenCard v-for="n in hiddenCardCount" :key="n" class="card" />
    </div>
    <div class="player-details">
      <div class="username"><NamePlate :name="username" /></div>
      <div class="score">Score: {{ score }}</div>
    </div>
  </div>
</template>

<script>
import HiddenCard from '@/components/HiddenCard.vue';
import NamePlate from '@/components/NamePlate.vue';

export default {
  name: 'NonSelfMatchPlayer',
  components: {
    HiddenCard,
    NamePlate
  },
  props: {
    username: String,
    hiddenCardCount: Number,
    highlightPlayer: Boolean,
    score: Number
  }
};
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';
@import '@/assets/cards/variables.css';
@import '@/assets/players';

.non-self-player {
  margin: calc(var(--card-height) / 2) 0 0 0;

  .hand {
    height: 0;
    .card {
      @include card-transform(-60deg, 0deg, 0, -1);
    }
  }
}
</style>
