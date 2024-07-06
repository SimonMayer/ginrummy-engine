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

.disabled {
  pointer-events: none;
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
