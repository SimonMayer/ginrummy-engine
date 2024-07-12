<template>
  <div class="stock-pile-container">
    <div class="stock-pile" :class="{ disabled: disabled, empty: isEmpty }" @click="handleClick">
      <HiddenCard v-for="n in size" :key="n" class="stock-card-item" />
      <div v-if="isEmpty" class="empty-placeholder"><div class="icon">↻</div>Rebuild from discards</div>
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
  computed: {
    isEmpty() {
      return this.size === 0;
    }
  }
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
  justify-content: left;
  position: relative;
  cursor: pointer;
  height: 150px;
  width: 150px;
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
  transform: rotate(-1.1deg);
}

.stock-card-item:nth-child(24n) {
  transform: rotate(-1.8deg);
}

.disabled {
  pointer-events: none;
  cursor: not-allowed;
}

.empty-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 150px;
  background-color: rgba(255, 255, 255, 0.8);
  border: 2px dashed #ccc;
  border-radius: 10px;
  font-size: 1.2em;
  color: #999;
}
</style>
