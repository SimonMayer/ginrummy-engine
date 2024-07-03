<template>
  <div class="match-list">
    <h1>Your Matches</h1>
    <ul>
      <li v-for="match in matches" :key="match.match_id">
        <p>Match ID: {{ match.match_id }}</p>
        <p>Start Time: {{ match.start_time }}</p>
        <p>End Time: {{ match.end_time }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      matches: [],
    };
  },
  async created() {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/matches', {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.matches = response.data;
    } catch (error) {
      alert('Failed to fetch matches!');
      console.error(error);
    }
  }
}
</script>

<style scoped>
.match-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background-color: #f9f9f9;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ddd;
}

p {
  margin: 5px 0;
}
</style>
