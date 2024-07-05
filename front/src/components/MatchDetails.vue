<template>
  <div class="match-details">
    <h1>Match ID: {{ matchId }}</h1>
    <div v-if="match">
      <p>Create Time: {{ formatDateTime(match.create_time) }}</p>
      <p v-if="match.start_time">Start Time: {{ formatDateTime(match.start_time) }}</p>
      <p v-if="match.end_time">End Time: {{ formatDateTime(match.end_time) }}</p>
      <h2>Stock Pile</h2>
      <StockPile :size="match.stock_pile_size" />
      <h2>Players</h2>
      <ul class="players-list">
        <li v-for="player in players" :key="player.user_id" class="player-item">
          {{ player.username }}
          <ul class="hand">
            <li v-for="n in player.handSize" :key="n" class="card-item">
              <HiddenCard />
            </li>
          </ul>
        </li>
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
import HiddenCard from './HiddenCard.vue';
import StockPile from './StockPile.vue';

export default {
  name: 'MatchDetails',
  components: {
    HiddenCard,
    StockPile
  },
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
    await this.loadHandsForPlayers();
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
    async loadHandsForPlayers() {
      try {
        if (this.match && this.match.current_round_id) {
          const response = await apiClient.get(`/rounds/${this.match.current_round_id}`);
          const hands = response.data.hands;

          this.players.forEach(player => {
            player.handSize = hands[player.user_id]?.size || 0;
          });

          this.match.stock_pile_size = response.data.stock_pile_size;
        }
      } catch (error) {
        alert('Failed to fetch hands!');
        console.error(error);
      }
    },
    async startMatch() {
      try {
        await apiClient.post(`/matches/${this.matchId}/start`);
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

.players-list {
  list-style-type: none;
  padding: 0;
  width: 100%;
}

.player-item {
  background-color: #f9f9f9;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ddd;
}

.hand {
  display: flex;
  flex-direction: row;
  padding: 0;
  margin: 10px 0 0 0;
  list-style-type: none;
}

.card-item:not(:first-child) {
  margin-left: -80px;
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
