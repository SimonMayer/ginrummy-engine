<template>
  <div class="match-details">
    <h1>Match ID: {{ matchId }}</h1>
    <div v-if="match">
      <p>Create Time: {{ formatDateTime(match.create_time) }}</p>
      <p v-if="match.start_time">Start Time: {{ formatDateTime(match.start_time) }}</p>
      <p v-if="match.end_time">End Time: {{ formatDateTime(match.end_time) }}</p>
      <h2>Players</h2>
      <ul>
        <li v-for="player in match.players" :key="player.user_id">{{ player.username }}</li>
      </ul>
    </div>
    <div v-else>
      <p>Loading match details...</p>
    </div>
  </div>
</template>

<script>
import apiClient from '../api/axios';
import { formatDateTime } from '../utils/dateFormatter';

export default {
  name: 'MatchDetails',
  data() {
    return {
      matchId: this.$route.params.id,
      match: null,
    };
  },
  async created() {
    await this.loadMatchDetails();
  },
  methods: {
    async loadMatchDetails() {
      try {
        const response = await apiClient.get(`/matches/${this.matchId}`);
        this.match = response.data;
      } catch (error) {
        alert('Failed to fetch match details!');
        console.error(error);
      }
    },
    formatDateTime
  }
};
</script>

<style scoped>
.match-details {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

h1, h2 {
  margin-bottom: 20px;
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
