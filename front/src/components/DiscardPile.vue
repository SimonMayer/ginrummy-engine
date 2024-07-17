<template>
  <div class="discard-pile">
    <VisibleCard
        ref="visibleCards"
        v-for="card in visibleCards"
        :key="card.card_id"
        :cardProp="card"
        :class="{ selectable: isCardSelectable(card), selected: isSelected(card) }"
        :selectable="isCardSelectable(card)"
        @update:selected="handleSelected"
    />
    <div v-if="isEmpty" class="empty-placeholder">
      <div>Discarded cards will appear here</div>
    </div>
  </div>
</template>

<script>
import VisibleCard from '@/components/VisibleCard.vue';
import visibleCardSelectionMixin from '@/mixins/visibleCardSelectionMixin';

export default {
  name: 'DiscardPile',
  components: {
    VisibleCard,
  },
  mixins: [visibleCardSelectionMixin],
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
    selectableCards: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    isEmpty() {
      return this.visibleCards.length === 0;
    }
  },
  methods: {
    isCardSelectable(card) {
      return this.selectableCards.includes(card);
    }
  }
};
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';
@import '@/assets/cards/variables.css';

.discard-pile {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: center;
  padding: calc(var(--card-height) * 0.1) calc(var(--card-width) * 0.1);
  height: var(--card-height);

  .selectable {
    cursor: pointer;
  }

  @for $i from 1 through 52 {
    .card:nth-child(#{$i}) {
      $rotate: rotate(0);
      @if $i == 1 {
        $rotate: rotate(0.6deg);
      } @else if $i % 5 == 0 {
        $rotate: rotate(-0.3deg);
      } @else if $i % 3 == 0 {
        $rotate: rotate(-1.2deg);
      } @else if $i % 2 == 0 {
        $rotate: rotate(-0.8deg);
      } @else if $i % 2 != 0 {
        $rotate: rotate(1deg);
      }
      transform: $rotate;

      @if $i != 1 {
        margin-left: calc(var(--card-width) * -0.85);
      }

      &.selected {
        transform: $rotate translateY(calc(var(--card-height) * -0.2));
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
      transform: rotate(-90deg);
      margin: var(--base-margin);
    }
  }
}
</style>
