<template>
  <div class="error-box">
    <p><strong>{{ title }}</strong></p>
    <p v-if="message">{{ message }}</p>
    <button class="close-button" @click="$emit('close')">X</button>
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
.error-box {
  border: 1px solid #b22222;
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  position: relative;
  max-width: 300px;
  margin: 10px 0;
  border-radius: 5px;
}

.close-button {
  position: absolute;
  top: 5px;
  right: 5px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #721c24;
}
</style>
