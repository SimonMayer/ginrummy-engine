<template>
  <div class="create-match">
    <h1>Create Match</h1>
    <button @click="createMatch">Create Match</button>
  </div>
</template>

<script>
import apiClient from '../api/axios';

export default {
  methods: {
    async createMatch() {
      try {
        const response = await apiClient.post('/matches');
        alert(`Match created! Match ID: ${response.data.match_id}`);
      } catch (error) {
        alert('Failed to create match!');
        console.error(error);
      }
    }
  }
}
</script>

<style scoped>
.create-match {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
