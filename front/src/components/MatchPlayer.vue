<template>
  <div :class="['player-item', { 'highlighted': highlightPlayer }]">
    {{ username }}
    <div class="hand" v-if="hiddenCardCount">
      <div v-for="n in hiddenCardCount" :key="n" class="card-item">
        <HiddenCard />
      </div>
    </div>
    <div class="hand" v-if="hand.length">
      <div
          v-for="card in hand"
          :key="card.card_id"
          :class="['card-item', { selectable: selectable, selected: isSelected(card) }]"
      >
        <VisibleCard ref="visibleCards" :cardProp="card" :selectable="selectable" @update:selected="handleSelected" />
      </div>
    </div>
  </div>
</template>

<script>
import HiddenCard from '@/components/HiddenCard.vue';
import VisibleCard from '@/components/VisibleCard.vue';

export default {
  name: 'MatchPlayer',
  components: {
    HiddenCard,
    VisibleCard
  },
  props: {
    username: {
      type: String,
      required: true
    },
    hand: {
      type: Array,
      required: true
    },
    hiddenCardCount: {
      type: Number,
      required: true,
      default: 0
    },
    highlightPlayer: {
      type: Boolean,
      default: false
    },
    selectable: {
      type: Boolean,
      default: false
    }
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

.player-item {
  background-color: rgba(var(--secondary-color-rgb), 0.2);
  color: var(--text-color);
  padding: var(--base-padding);
  margin: var(--base-margin) 0;
  border: 1px solid var(--secondary-color);
  border-radius: var(--border-radius);

  &.highlighted {
    border: 2px solid var(--primary-color);
    background-color: var(--tertiary-color);
  }

  .hand {
    display: flex;
    flex-direction: row;
    padding: 0;
    margin: var(--base-margin) 0 0 0;

    .card-item {
      transition: transform 0.3s ease;

      &.selectable {
        cursor: pointer;
      }

      &.selected {
        transform: translateY(-20px);
      }

      &:not(:first-child) {
        margin-left: calc(var(--card-width) * -0.8);
      }
    }
  }
}
</style>
