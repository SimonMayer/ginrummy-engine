<template>
  <div class="player-item non-self-player" :class="{ 'highlighted': highlightPlayer }">
    {{ username }}
    <div class="hand">
      <HiddenCard v-for="n in hiddenCardCount" :key="n" class="card" />
    </div>
    <div class="melds-container">
      <PlayedMeld
          v-for="meld in melds"
          :key="meld.meld_id"
          :id="meld.meld_id"
          :type="meld.meld_type"
          :cards="meld.cards"
      />
    </div>
  </div>
</template>

<script>
import HiddenCard from '@/components/HiddenCard.vue';
import PlayedMeld from '@/components/PlayedMeld.vue';

export default {
  name: 'NonSelfMatchPlayer',
  components: {
    HiddenCard,
    PlayedMeld
  },
  props: {
    username: String,
    hiddenCardCount: Number,
    highlightPlayer: Boolean,
    melds: Array
  }
};
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';
@import '@/assets/cards/variables.css';
@import '@/assets/players';
.hand {
  .card {
    @include card-transform(0deg, 0, -1);

    &.selected {
      @include card-transform(3deg, calc(var(--card-height) / -5), -1);
    }
  }
}
</style>
