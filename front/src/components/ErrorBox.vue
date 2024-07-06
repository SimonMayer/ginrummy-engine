<template>
  <div class="error-box" v-if="message">
    <p>{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'ErrorBox',
  props: {
    message: {
      type: String,
      required: true
    }
  }
};
</script>

<style scoped>
.error-box {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
  width: 100%;
  text-align: center;
}
</style>
