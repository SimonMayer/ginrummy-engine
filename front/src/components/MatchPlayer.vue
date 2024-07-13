<template>
  <li :class="['player-item', { 'highlighted': highlightPlayer }]">
    {{ username }}
    <ul class="hand" v-if="hiddenCardCount">
      <li v-for="n in hiddenCardCount" :key="n" class="card-item">
        <HiddenCard />
      </li>
    </ul>
    <ul class="hand" v-if="hand.length">
      <li
          v-for="card in hand"
          :key="card.card_id"
          :class="['card-item', { selectable: selectable }]"
      >
        <VisibleCard ref="visibleCards" :cardProp="card" :selectable="selectable" />
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
  methods: {
    getSelectedCards() {
      if (!this.$refs.visibleCards) {
        return [];
      }
      return this.$refs.visibleCards.filter(visibleCard => visibleCard.isCardSelected());
    }
  }
};
</script>

<style scoped>
.player-item {
  background-color: rgba(var(--secondary-color-rgb), 0.2);
  color: var(--text-color);
  padding: var(--base-padding);
  margin: var(--base-margin) 0;
  border: 1px solid var(--secondary-color);
  border-radius: var(--border-radius);
}

.highlighted {
  border: 2px solid var(--primary-color);
  background-color: var(--tertiary-color);
}

.hand {
  display: flex;
  flex-direction: row;
  padding: 0;
  margin: var(--base-margin) 0 0 0;
  list-style-type: none;
}

.card-item {
  transition: transform 0.3s ease;
}

.card-item.selectable {
  cursor: pointer;
}

.card-item.selected {
  transform: translateY(-20px);
}

.card-item:not(:first-child) {
  margin-left: -80px;
}
</style>
