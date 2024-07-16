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
@mixin fan-shape($num-cards, $span, $offset-rotation) {
  @for $i from 1 through $num-cards {
    $rotation: (($i - calc($num-cards / 2)) * calc($span / $num-cards) + $offset-rotation);
    .card:nth-child(#{$i}) {
      transform: rotate($rotation);
    }
  }
}

.meld {
  position: relative;
  display: flex;
  justify-content: right;
  align-items: flex-start;

  .card {
    position: absolute;
    transform-origin: bottom left;
    transition: transform 0.3s;
  }

  &.run {
    width: calc(var(--card-width) * 1.7);
    height: calc(var(--card-height) + calc(var(--card-width) * 0.5));
    padding: calc(var(--card-height) / 6) calc(var(--card-width) * 0.5) 0 0;
    @include fan-shape(13, 90deg, 10);
  }

  &.set {
    width: calc(var(--card-width) + (var(--card-height) / 4));
    height: calc(var(--card-height) + (var(--card-width) / 4));
    padding: calc(var(--card-height) / 10) calc(var(--card-width) / 5) 0 0;
    @include fan-shape(4, 30deg, -5);
  }
}
</style>
