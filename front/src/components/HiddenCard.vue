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
  background-image:
      linear-gradient(
          90deg,
          transparent 15%,
          rgba(215, 215, 72, 0.5) 15%,
          rgba(215, 215, 72, 0.5) 30%,
          transparent 30%,
          transparent 50%,
          rgba(215, 215, 72, 0.5) 50%,
          rgba(215, 215, 72, 0.5) 65%,
          transparent 65%,
          transparent 85%,
          rgba(215, 215, 72, 0.5) 85%,
          rgba(215, 215, 72, 0.5) 100%
      ),
      linear-gradient(
          transparent 15%,
          rgba(215, 215, 72, 0.5) 15%,
          rgba(215, 215, 72, 0.5) 30%,
          transparent 30%,
          transparent 50%,
          rgba(215, 215, 72, 0.5) 50%,
          rgba(215, 215, 72, 0.5) 65%,
          transparent 65%,
          transparent 85%,
          rgba(215, 215, 72, 0.5) 85%,
          rgba(215, 215, 72, 0.5) 100%
      ),
      linear-gradient(
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
          90deg,
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
          135deg,
          transparent 25%,
          rgba(90, 0, 40, 0.5) 25%,
          rgba(90, 0, 40, 0.5) 35%,
          transparent 35%,
          transparent 75%,
          rgba(90, 0, 40, 0.5) 75%,
          rgba(90, 0, 40, 0.5) 85%,
          transparent 85%
      ),
      linear-gradient(
          45deg,
          transparent 25%,
          rgba(90, 0, 40, 0.5) 25%,
          rgba(90, 0, 40, 0.5) 35%,
          transparent 35%,
          transparent 75%,
          rgba(90, 0, 40, 0.5) 75%,
          rgba(90, 0, 40, 0.5) 85%,
          transparent 85%
      );
  background-size: 40px 40px;
}
</style>
