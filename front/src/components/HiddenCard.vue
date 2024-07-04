<template>
  <div class="card hidden-card"></div>
</template>

<script>
export default {
  name: 'HiddenCard'
};
</script>

<style scoped>
@import '../assets/cardStyles.css';

.hidden-card {
  background: linear-gradient(45deg, #3b3b3b, #696969);
}
</style>
