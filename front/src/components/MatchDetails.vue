<template>
  <div class="match-details">
    <h1>Match ID: {{ matchId }}</h1>
    <ErrorBox v-if="errorMessage" :message="errorMessage" />
    <LoadingIndicator :visible="loading" />
    <div v-if="match">
      <p>Create Time: {{ formatDateTime(match.create_time) }}</p>
      <p v-if="match.start_time">Start Time: {{ formatDateTime(match.start_time) }}</p>
      <p v-if="match.end_time">End Time: {{ formatDateTime(match.end_time) }}</p>
      <h2>Stock Pile</h2>
      <StockPile
          v-if="match.stock_pile_size !== undefined"
          :size="match.stock_pile_size"
          @click="handleStockPileClick"
          :disabled="loading"
      />
      <h2>Players</h2>
      <ul class="players-list">
        <li
            v-for="player in players"
            :key="player.user_id"
            :class="{ 'current-turn': isCurrentTurn(player.user_id) }"
            class="player-item"
        >
          {{ player.username }}
          <ul class="hand" v-if="player.user_id !== signedInUserId">
            <li v-for="n in player.handSize" :key="n" class="card-item">
              <HiddenCard />
            </li>
          </ul>
          <ul class="hand" v-else>
            <li v-for="card in myHand" :key="card.card_id" class="card-item">
              <VisibleCard :card="card" />
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
import {formatDateTime} from '../utils/dateFormatter';
import HiddenCard from './HiddenCard.vue';
import StockPile from './StockPile.vue';
import VisibleCard from './VisibleCard.vue';
import ErrorBox from './ErrorBox.vue';
import LoadingIndicator from './LoadingIndicator.vue';

export default {
  name: 'MatchDetails',
  components: {
    HiddenCard,
    StockPile,
    VisibleCard,
    ErrorBox,
    LoadingIndicator,
  },
  data() {
    return {
      matchId: this.$route.params.id,
      match: null,
      players: [],
      minPlayers: 2,
      maxPlayers: 4,
      signedInUserId: parseInt(localStorage.getItem('user_id'), 10),
      myHand: [],
      currentTurnUserId: null,
      turnId: null,
      loading: true, // Set initial loading state to true
      errorMessage: '',
    };
  },
  async created() {
    try {
      await this.loadMatchDetails();
      await this.loadPlayers();
      await this.loadHandsForPlayers();
      await this.loadMyHand();
      await this.loadCurrentTurn();
    } catch (error) {
      this.errorMessage = error.message;
    } finally {
      this.loading = false; // Set loading to false after data is fetched
    }
  },
  methods: {
    async fetchData(endpoint, errorMessage) {
      try {
        const response = await apiClient.get(endpoint);
        return response.data;
      } catch (error) {
        this.errorMessage = errorMessage;
        console.error(error);
        throw error;
      }
    },
    async loadMatchDetails() {
      this.match = await this.fetchData(
          `/matches/${this.matchId}`,
          'Failed to fetch match details!'
      );
    },
    async loadPlayers() {
      this.players = await this.fetchData(
          `/matches/${this.matchId}/players`,
          'Failed to fetch players!'
      );
    },
    async loadHandsForPlayers() {
      if (this.match && this.match.current_round_id) {
        const data = await this.fetchData(
            `/rounds/${this.match.current_round_id}`,
            'Failed to fetch hands!'
        );
        const hands = data.hands;

        this.players.forEach((player) => {
          player.handSize = hands[player.user_id]?.size || 0;
        });

        this.match.stock_pile_size = data.stock_pile_size || 0;
      }
    },
    async loadMyHand() {
      if (this.match && this.match.current_round_id) {
        const data = await this.fetchData(
            `/rounds/${this.match.current_round_id}/my_hand`,
            'Failed to fetch your hand!'
        );
        this.myHand = data.cards;
      }
    },
    async loadCurrentTurn() {
      if (this.match && this.match.current_round_id) {
        const data = await this.fetchData(
            `/rounds/${this.match.current_round_id}/current_turn`,
            'Failed to fetch current turn!'
        );
        this.currentTurnUserId = data.user_id;
        this.turnId = data.turn_id;
      }
    },
    async handleStockPileClick() {
      if (this.currentTurnUserId === this.signedInUserId && !this.loading) {
        this.loading = true;
        try {
          const response = await apiClient.post(
              `/turns/${this.turnId}/draw_from_stock_pile`
          );
          this.myHand.push(response.data.new_card);
          this.match.stock_pile_size -= 1;
        } catch (error) {
          this.errorMessage = 'Failed to draw from stock pile!';
          console.error(error);
        } finally {
          this.loading = false;
        }
      }
    },
    async startMatch() {
      if (!this.loading) {
        this.loading = true;
        try {
          await apiClient.post(`/matches/${this.matchId}/start`);
          await this.loadMatchDetails();
        } catch (error) {
          this.errorMessage = 'Failed to start match!';
          console.error(error);
        } finally {
          this.loading = false;
        }
      }
    },
    formatDateTime,
    isCurrentTurn(userId) {
      return this.currentTurnUserId === userId;
    },
  },
  computed: {
    canStartMatch() {
      return (
          this.players.length >= this.minPlayers &&
          this.players.length <= this.maxPlayers &&
          !this.match.start_time
      );
    },
  },
};
</script>

<style scoped>
.match-details {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

h1,
h2 {
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

.current-turn {
  border: 2px solid #4caf50;
  background-color: #e8f5e9;
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
  background-color: #4caf50;
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
