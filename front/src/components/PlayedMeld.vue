<template>
  <div :class="['meld', type]">
    <VisibleCard
        v-for="card in cards"
        :key="card.card_id"
        :cardProp="card"
        :selectable="false"
        class="card"
    />
  </div>
</template>

<script>
import VisibleCard from '@/components/VisibleCard.vue';

export default {
  name: 'PlayedMeld',
  components: {
    VisibleCard
  },
  props: {
    cards: {
      type: Array,
      required: true
    },
    id: {
      type: Number,
      required: true
    },
    type: {
      type: String,
      required: true
    }
  }
};
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';
@import '@/assets/cards/variables.css';
@mixin fan-shape($num-cards, $span) {
  @for $i from 1 through $num-cards {
    $rotation: (($i - ($num-cards / 2)) * ($span / $num-cards));
    .card:nth-child(#{$i}) {
      transform: rotate($rotation);
    }
  }
}

.meld {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;

  .card {
    position: absolute;
    transform-origin: bottom left;
    transition: transform 0.3s;
  }

  &.set {
    width: calc(var(--card-width) + (var(--card-height) / 2));
    height: calc(var(--card-height) + (var(--card-width) / 2));
    @include fan-shape(4, 30deg); // Up to 4 cards
  }
}
</style>
