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
  background-color: #001f3f;
  background-image: linear-gradient(
      #001f3f 1px,
      transparent 5px,
      transparent 100%
  ),
  linear-gradient(
      to left,
      #001f3f 1px,
      transparent 5px,
      transparent 100%
  ),
  linear-gradient(
      to top,
      #001f3f 1px,
      transparent 5px,
      transparent 100%
  ),
  linear-gradient(
      to right,
      #001f3f 1px,
      transparent 5px,
      transparent 100%
  ),
  linear-gradient(
      30deg,
      transparent 12%,
      rgba(90, 0, 40, 0.5) 12%,
      rgba(90, 0, 40, 0.5) 13%,
      transparent 13%,
      transparent 32%,
      rgba(90, 0, 40, 0.5) 32%,
      rgba(90, 0, 40, 0.5) 33%,
      transparent 33%,
      transparent 67%,
      rgba(90, 0, 40, 0.5) 67%,
      rgba(90, 0, 40, 0.5) 68%,
      transparent 68%,
      transparent 87%,
      rgba(90, 0, 40, 0.5) 87%,
      rgba(90, 0, 40, 0.5) 88%,
      transparent 88%,
      transparent 100%
  ),
  linear-gradient(
      120deg,
      transparent 45%,
      rgba(90, 0, 40, 0.5) 45%,
      rgba(90, 0, 40, 0.5) 46%,
      transparent 46%,
      transparent 54%,
      rgba(90, 0, 40, 0.5) 54%,
      rgba(90, 0, 40, 0.5) 55%,
      transparent 55%,
      transparent 100%
  ),
  linear-gradient(
      120deg,
      transparent 10%,
      rgba(215, 215, 72, 0.5) 10%,
      rgba(215, 215, 72, 0.5) 15%,
      transparent 15%,
      transparent 20%,
      rgba(215, 215, 72, 0.5) 20%,
      rgba(215, 215, 72, 0.5) 25%,
      transparent 25%,
      transparent 30%,
      rgba(215, 215, 72, 0.5) 30%,
      rgba(215, 215, 72, 0.5) 35%,
      transparent 35%,
      transparent 42%,
      rgba(215, 215, 72, 0.5) 42%,
      rgba(215, 215, 72, 0.5) 49.5%,
      transparent 49.5%,
      transparent 50.5%,
      rgba(215, 215, 72, 0.5) 50.5%,
      rgba(215, 215, 72, 0.5) 58%,
      transparent 58%,
      transparent 65%,
      rgba(215, 215, 72, 0.5) 65%,
      rgba(215, 215, 72, 0.5) 70%,
      transparent 70%,
      transparent 75%,
      rgba(215, 215, 72, 0.5) 75%,
      rgba(215, 215, 72, 0.5) 80%,
      transparent 80%,
      transparent 85%,
      rgba(215, 215, 72, 0.5) 85%,
      rgba(215, 215, 72, 0.5) 90%,
      transparent 90%,
      transparent 100%
  ),
  linear-gradient(
      30deg,
      transparent 10%,
      rgba(215, 215, 72, 0.5) 10%,
      rgba(215, 215, 72, 0.5) 15%,
      transparent 15%,
      transparent 20%,
      rgba(215, 215, 72, 0.5) 20%,
      rgba(215, 215, 72, 0.5) 25%,
      transparent 25%,
      transparent 30%,
      rgba(215, 215, 72, 0.5) 30%,
      rgba(215, 215, 72, 0.5) 35%,
      transparent 35%,
      transparent 42%,
      rgba(215, 215, 72, 0.5) 42%,
      rgba(215, 215, 72, 0.5) 49.5%,
      transparent 49.5%,
      transparent 50.5%,
      rgba(215, 215, 72, 0.5) 50.5%,
      rgba(215, 215, 72, 0.5) 58%,
      transparent 58%,
      transparent 65%,
      rgba(215, 215, 72, 0.5) 65%,
      rgba(215, 215, 72, 0.5) 70%,
      transparent 70%,
      transparent 75%,
      rgba(215, 215, 72, 0.5) 75%,
      rgba(215, 215, 72, 0.5) 80%,
      transparent 80%,
      transparent 85%,
      rgba(215, 215, 72, 0.5) 85%,
      rgba(215, 215, 72, 0.5) 90%,
      transparent 90%,
      transparent 100%
  ),
  linear-gradient(
      120deg,
      transparent 15%,
      rgba(0, 70, 90, 0.3) 15%,
      rgba(0, 70, 90, 0.3) 30%,
      transparent 30%,
      transparent 50%,
      rgba(0, 70, 90, 0.3) 50%,
      rgba(0, 70, 90, 0.3) 65%,
      transparent 65%,
      transparent 85%,
      rgba(0, 70, 90, 0.3) 85%,
      rgba(0, 70, 90, 0.3) 100%
  ),
  linear-gradient(
      30deg,
      transparent 15%,
      rgba(0, 70, 90, 0.3) 15%,
      rgba(0, 70, 90, 0.3) 30%,
      transparent 30%,
      transparent 50%,
      rgba(0, 70, 90, 0.3) 50%,
      rgba(0, 70, 90, 0.3) 65%,
      transparent 65%,
      transparent 85%,
      rgba(0, 70, 90, 0.3) 85%,
      rgba(0, 70, 90, 0.3) 100%
  );
}
</style>
