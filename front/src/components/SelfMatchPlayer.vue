<template>
  <div class="player-item self-player">
    <div v-if="highlightPlayer" class="highlight-container">
      <div :class="{ 'highlight': highlightPlayer }"></div>
    </div>
    <div class="player-details">
      <div class="username"><NamePlate :name="username" /></div>
      <div class="score">Score: {{ score }}</div>
    </div>
    <div class="hand">
      <VisibleCard
          ref="visibleCards"
          v-for="card in hand"
          :key="card.card_id"
          :cardProp="card"
          :class="['card', { selectable: selectable, selected: isSelected(card) }]"
          :selectable="selectable"
          @update:selected="handleSelected"
      />
    </div>
  </div>
</template>

<script>
import VisibleCard from '@/components/VisibleCard.vue';
import NamePlate from "@/components/NamePlate.vue";
import visibleCardSelectionMixin from '@/mixins/visibleCardSelectionMixin';

export default {
  name: 'SelfMatchPlayer',
  components: {
    NamePlate,
    VisibleCard
  },
  mixins: [visibleCardSelectionMixin],
  props: {
    username: String,
    hand: Array,
    highlightPlayer: Boolean,
    selectable: Boolean,
    score: Number
  }
};
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';
@import '@/assets/cards/variables.css';
@import '@/assets/players';

.highlight-container {
  justify-content: left;
}

.hand {
  height: var(--card-height);
  margin: calc(var(--base-margin) * 2) 0 0 0;
  padding: 0 var(--card-width);

  .card {
    @include card-transform(-40deg, 0deg, 0, 0.2);

    &.selected {
      @include card-transform(-40deg, 3deg, calc(var(--card-height) / -5), 0.2);
    }
  }
}
</style>
