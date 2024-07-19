<template>
  <div class="stock-pile-container">
    <div class="stock-pile" :class="{ disabled: disabled, empty: isEmpty }" @click="handleClick">
      <HiddenCard v-for="n in size" :key="n" class="stock-card-item" />
      <div v-if="isEmpty" class="empty-placeholder">
        <div class="icon">↻</div>
        <div>Rebuild from discards</div>
      </div>
    </div>
  </div>
</template>

<script>
import HiddenCard from '@/components/HiddenCard.vue';

export default {
  name: 'StockPile',
  components: {
    HiddenCard,
  },
  props: {
    size: {
      type: Number,
      required: true,
      validator: value => value >= 0 // Ensure size is a non-negative number
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    handleClick() {
      if (!this.disabled) {
        this.$emit('click');
      }
    },
  },
  computed: {
    isEmpty() {
      return this.size === 0;
    }
  }
};
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';
@import '@/assets/cards/variables.css';

.stock-pile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: var(--base-margin);
}

.stock-pile {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: left;
  position: relative;
  cursor: pointer;
  height: var(--card-height);
  width: calc(var(--card-width) * 1.5);

  @for $i from 1 through 52 {
    .stock-card-item:nth-child(#{$i}) {
      @if $i % 24 == 0 {
        transform: rotate(-1.8deg);
      }
      @else if $i % 11 == 0 {
        transform: rotate(-1.1deg);
      }
      @else if $i % 7 == 0 {
        transform: rotate(-0.5deg);
      }
      @else if $i % 5 == 0 {
        transform: rotate(0.4deg);
      }
      @else if $i % 2 == 0 {
        transform: rotate(0.2deg);
      }
      @else if $i % 2 != 0 {
        transform: rotate(-0.3deg);
      }

      @if $i != 1 {
        margin-left: calc(var(--card-width) * -1);
      }
    }
  }

  &.disabled {
    pointer-events: none;
    cursor: not-allowed;
  }

  .empty-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
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
