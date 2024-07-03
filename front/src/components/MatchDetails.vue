<template>
  <div class="match-details">
    <h1>Match ID: {{ matchId }}</h1>
    <div v-if="match">
      <p>Create Time: {{ formatDateTime(match.create_time) }}</p>
      <p v-if="match.start_time">Start Time: {{ formatDateTime(match.start_time) }}</p>
      <p v-if="match.end_time">End Time: {{ formatDateTime(match.end_time) }}</p>
      <h2>Players</h2>
      <ul>
        <li v-for="player in players" :key="player.user_id">{{ player.username }}</li>
      </ul>
      <button v-if="canStartMatch" @click="startMatch">Start Match</button>
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
      players: [],
      minPlayers: 2,
      maxPlayers: 4
    };
  },
  async created() {
    await this.loadMatchDetails();
    await this.loadPlayers();
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
    async loadPlayers() {
      try {
        const response = await apiClient.get(`/matches/${this.matchId}/players`);
        this.players = response.data;
      } catch (error) {
        alert('Failed to fetch players!');
        console.error(error);
      }
    },
    async startMatch() {
      try {
        await apiClient.post(`/matches/${this.matchId}/start`);
        // Reload match details to get the updated start time
        await this.loadMatchDetails();
      } catch (error) {
        alert('Failed to start match!');
        console.error(error);
      }
    },
    formatDateTime
  },
  computed: {
    canStartMatch() {
      return this.players.length >= this.minPlayers && this.players.length <= this.maxPlayers && !this.match.start_time;
    }
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

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 3px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}
</style>
