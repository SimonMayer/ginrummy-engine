<template>
  <div class="discard-pile">
    <VisibleCard
        v-for="card in visibleCards"
        :key="card.card_id"
        :cardProp="card"
    />
  </div>
</template>

<script>
import VisibleCard from './VisibleCard.vue';

export default {
  name: 'DiscardPile',
  components: {
    VisibleCard,
  },
  props: {
    visibleCards: {
      type: Array,
      required: true,
      validator(value) {
        return value.every(card => (
            typeof card.card_id === 'number' &&
            typeof card.rank === 'string' &&
            typeof card.suit === 'string' &&
            typeof card.point_value === 'number'
        ));
      },
    },
  },
};
</script>

<style scoped>
.discard-pile {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 10px;
}

.card:not(:first-child) {
  margin-left: -75px;
}

.card:first-child {
  transform: rotate(0.6deg);
}

.card:nth-child(even) {
  transform: rotate(-0.8deg);
}

.card:nth-child(odd) {
  transform: rotate(1deg);
}

.card:nth-child(3n) {
  transform: rotate(-1.2deg);
}

.card:nth-child(5n) {
  transform: rotate(-0.3deg);
}

</style>
