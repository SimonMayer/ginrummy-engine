<template>
  <div class="corner">
    <div>{{ rank }}</div>
    <div>{{ suit }}</div>
  </div>
</template>

<script>
export default {
  name: 'CardCorner',
  props: {
    rank: {
      type: String,
      required: true,
    },
    suit: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.corner {
  width: 20px;
  font-size: 12px;
  position: absolute;
}
</style>
