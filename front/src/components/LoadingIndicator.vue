<template>
  <transition name="fade">
    <div v-if="visible" class="loading-overlay">
      <div class="spinner"></div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'LoadingIndicator',
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';

.loading-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 1;
  pointer-events: none;

  .spinner {
    border: 0.3em solid rgba(0, 0, 0, 0.1);
    border-top: 0.3em solid #333;
    border-radius: 50%;
    width: 3rem;
    height: 3rem;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
