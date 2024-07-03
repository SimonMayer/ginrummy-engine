<template>
  <div class="match-list">
    <h1>Your Matches</h1>
    <ul>
      <li v-for="match in sortedMatches" :key="match.match_id">
        <p>Match ID: {{ match.match_id }}</p>
        <p>Start Time: {{ formatDateTime(match.start_time) }}</p>
        <p v-if="match.end_time">End Time: {{ formatDateTime(match.end_time) }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
import apiClient from '../api/axios';
import { formatDateTime } from '../utils/dateFormatter';

export default {
  name: 'MatchList',
  data() {
    return {
      matches: [],
    };
  },
  async created() {
    try {
      const response = await apiClient.get('/matches');
      this.matches = response.data;
    } catch (error) {
      alert('Failed to fetch matches!');
      console.error(error);
    }
  },
  computed: {
    sortedMatches() {
      return this.matches.slice().sort((a, b) => new Date(b.start_time) - new Date(a.start_time));
    }
  },
  methods: {
    formatDateTime
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
