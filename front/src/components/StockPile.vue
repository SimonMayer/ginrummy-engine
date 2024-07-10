<template>
  <div class="stock-pile-container">
    <div class="stock-pile" :class="{ disabled: disabled }" @click="handleClick">
      <HiddenCard v-for="n in size" :key="n" class="stock-card-item" />
    </div>
  </div>
</template>

<script>
import HiddenCard from './HiddenCard.vue';

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
};
</script>

<style scoped>
.stock-pile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.stock-pile {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  position: relative;
  cursor: pointer;
}

.stock-card-item:not(:first-child) {
  margin-left: -100px;
}

.stock-card-item:nth-child(odd) {
  transform: rotate(-0.3deg);
}

.stock-card-item:nth-child(2n) {
  transform: rotate(0.2deg);
}

.stock-card-item:nth-child(5n) {
  transform: rotate(0.4deg);
}

.stock-card-item:nth-child(7n) {
  transform: rotate(-0.5deg);
}

.stock-card-item:nth-child(11n) {
  transform: rotate(0.7deg);
}

.disabled {
  pointer-events: none;
  cursor: not-allowed;
}
</style>
