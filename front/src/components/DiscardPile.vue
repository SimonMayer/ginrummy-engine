<template>
  <div class="discard-pile">
    <VisibleCard
        v-for="(card, index) in visibleCards"
        :key="card.card_id"
        :cardProp="card"
        :class="{ clickable: isTopCard(index) }"
        :clickable="isTopCard(index)"
        @card-clicked="handleClick(index)"
    />
    <div v-if="isEmpty" class="empty-placeholder">
      <div>Discarded cards will appear here</div>
    </div>
  </div>
</template>

<script>
import VisibleCard from '@/components/VisibleCard.vue';

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
  computed: {
    isEmpty() {
      return this.visibleCards.length === 0;
    }
  },
  methods: {
    isTopCard(index) {
      return index === this.visibleCards.length - 1;
    },
    handleClick() {
      this.$emit('top-card-clicked');
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';
@import '@/assets/cards/variables.css';

.discard-pile {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  padding: calc(var(--card-height) * 0.1) calc(var(--card-width) * 0.1);
  height: var(--card-height);

  .clickable {
    cursor: pointer;
  }

  @for $i from 1 through 52 {
    .card:nth-child(#{$i}) {
      @if $i == 1 {
        transform: rotate(0.6deg);
      } @else if $i % 5 == 0 {
        transform: rotate(-0.3deg);
      } @else if $i % 3 == 0 {
        transform: rotate(-1.2deg);
      } @else if $i % 2 == 0 {
        transform: rotate(-0.8deg);
      } @else if $i % 2 != 0 {
        transform: rotate(1deg);
      }

      @if $i != 1 {
        margin-left: calc(var(--card-width) * -0.85);
      }
    }
  }

  .empty-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    width: var(--card-width);
    height: var(--card-height);
    background-color: rgba(var(--secondary-color-rgb), 0.8);
    border: calc(var(--card-border-width) * 5) dashed var(--disabled-color);
    border-radius: var(--card-border-radius);
    font-size: calc(var(--card-base-size) * 18);
    color: var(--disabled-color);

    div {
      margin: var(--base-margin);
    }
  }
}
</style>
