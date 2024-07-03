<template>
  <div class="match-details">
    <h1>Match ID: {{ matchId }}</h1>
    <h2>Players</h2>
    <ul>
      <li v-for="player in players" :key="player.user_id">{{ player.username }}</li>
    </ul>
  </div>
</template>

<script>
import apiClient from '../api/axios';

export default {
  name: 'MatchDetails',
  data() {
    return {
      matchId: this.$route.params.id,
      players: [],
    };
  },
  async created() {
    await this.loadMatchDetails();
  },
  methods: {
    async loadMatchDetails() {
      try {
        const response = await apiClient.get(`/matches/${this.matchId}/players`);
        this.players = response.data;
      } catch (error) {
        alert('Failed to fetch match details!');
        console.error(error);
      }
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
</style>
