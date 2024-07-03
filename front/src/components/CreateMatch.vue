<template>
  <div class="create-match">
    <h1>Create Match</h1>
    <button @click="createMatch">Create Match</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    async createMatch() {
      const token = localStorage.getItem('token');
      try {
        const response = await axios.post('http://localhost:5000/matches', {}, {
          headers: {Authorization: `Bearer ${token}`}
        });
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
  margin-top: 50px;
}

h1 {
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #008CBA;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #007B9E;
}
</style>
