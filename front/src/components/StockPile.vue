<template>
  <div class="stock-pile">
    <HiddenCard v-for="n in size" :key="n" class="stock-card-item" />
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
  },
};
</script>

<style scoped>
.stock-pile {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  position: relative;
}

.stock-card-item:not(:first-child) {
  margin-left: -100px;
}
</style>
