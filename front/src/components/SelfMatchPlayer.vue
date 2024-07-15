<template>
  <div class="player-item self-player" :class="{ 'highlighted': highlightPlayer }">
    {{ username }}
    <div class="melds-container">
      <PlayedMeld
          v-for="meld in melds"
          :key="meld.meld_id"
          :id="meld.meld_id"
          :type="meld.meld_type"
          :cards="meld.cards"
      />
    </div>
    <div class="hand">
      <VisibleCard
          ref="visibleCards"
          v-for="card in hand"
          :key="card.card_id"
          :class="['card', { selectable: selectable, selected: isSelected(card) }]"
          :cardProp="card"
          :selectable="selectable"
          @update:selected="handleSelected"
      />
    </div>
  </div>
</template>

<script>
import VisibleCard from '@/components/VisibleCard.vue';
import PlayedMeld from '@/components/PlayedMeld.vue';

export default {
  name: 'SelfMatchPlayer',
  components: {
    VisibleCard,
    PlayedMeld
  },
  props: {
    username: String,
    hand: Array,
    highlightPlayer: Boolean,
    selectable: Boolean,
    melds: Array
  },
  data() {
    return {
      selectedCards: []
    };
  },
  methods: {
    getSelectedCards() {
      if (!this.$refs.visibleCards) {
        return [];
      }
      return this.$refs.visibleCards.filter(visibleCard => visibleCard.isCardSelected());
    },
    handleSelected() {
      this.selectedCards = this.getSelectedCards().map(card => card.cardProp.card_id);
    },
    isSelected(card) {
      return this.selectedCards.includes(card.card_id);
    }
  }
};
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';
@import '@/assets/cards/variables.css';
@import '@/assets/players';

.hand {
  margin: calc(var(--base-margin) * 2) 0 0 0;

  .card {
    @include card-transform(0deg, 0, 0.4);

    &.selected {
      @include card-transform(3deg, calc(var(--card-height) / -5), 0.4);
    }
  }
}
</style>
