<template>
  <div class="pattern">
    <div v-for="n in suitRepeat" :key="n" class="suit-symbol">{{ suitEmoji }}</div>
  </div>
</template>

<script>
export default {
  name: 'CardPattern',
  props: {
    suitEmoji: {
      type: String,
      required: true,
    },
    suitRepeat: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style scoped>
.pattern {
  position: absolute;
  top: 10px;
  bottom: 10px;
  left: 20px;
  right: 20px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(16, 1fr);
  justify-content: center;
  justify-items: center;
  align-items: center;
}

.suit-symbol {
  font-size: 20px;
}
</style>
