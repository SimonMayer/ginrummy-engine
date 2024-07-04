<template>
  <div class="playing-card">
    {{ card.rank }} of {{ card.suit }} (Points: {{ card.point_value }})
  </div>
</template>

<script>
export default {
  name: 'PlayingCard',
  props: {
    card: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
.playing-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  margin: 5px;
  text-align: center;
}
</style>
