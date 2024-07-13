<template>
  <div class="wrapper">
    <div class="error-box">
      <div class="title">{{ title }}</div>
      <div v-if="message" class="message">{{ message }}</div>
      <div class="close-button" @click="$emit('close')"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ErrorBox',
  props: {
    title: {
      type: String,
      required: true
    },
    message: {
      type: String,
      default: ''
    }
  }
};
</script>

<style scoped>
.wrapper {
  background-color: white;
  border-radius: 5px;
  margin: 10px 0 40px;
  min-width: 400px;
  padding: 2px;

}
.error-box {
  border: 1px solid var(--error-accent-color);
  color: var(--text-color);
  position: relative;
  border-radius: 5px;
}

.title {
  background-color: var(--error-color);
  font-weight: bold;
  min-height: 30px;
  padding: 10px;
}

.message {
  color: var(--error-color);
  min-height: 20px;
  padding: 10px;
}
.close-button {
  border-radius: 5px;
  position: absolute;
  top: 5px;
  right: 5px;
  cursor: pointer;
  padding: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
  width: 12px;
  height: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button::before,
.close-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 16px;
  height: 3px;
  background: var(--text-color);
  transform-origin: center;
}

.close-button::before {
  transform: translate(-50%, -50%) rotate(45deg);
}

.close-button::after {
  transform: translate(-50%, -50%) rotate(-45deg);
}
.close-button:hover {
  background-color: var(--error-accent-color);
}
.close-button:active {
  background-color: var(--button-active-color);
}
</style>
