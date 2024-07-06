<template>
  <div class="match-details">
    <h1>Match ID: {{ matchId }}</h1>
    <ErrorBox v-if="errorMessage" :message="errorMessage" @close="clearErrorMessage" />
    <LoadingIndicator :visible="loading" />
    <div v-if="match">
      <StockPile
          v-if="match.stock_pile_size !== undefined"
          :size="match.stock_pile_size"
          @click="handleStockPileClick"
          :disabled="loading"
      />
      <ul class="players-list">
        <MatchPlayer
            v-for="player in players"
            :key="player.user_id"
            :player="player"
            :myHand="myHand"
            :signedInUserId="signedInUserId"
            :currentTurnUserId="currentTurnUserId"
        />
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
import StockPile from './StockPile.vue';
import ErrorBox from './ErrorBox.vue';
import LoadingIndicator from './LoadingIndicator.vue';
import MatchPlayer from './MatchPlayer.vue';

export default {
  name: 'MatchDetails',
  components: {
    StockPile,
    ErrorBox,
    LoadingIndicator,
    MatchPlayer
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
      loading: true,
      errorMessage: ''
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
      this.loading = false;
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
    async postData(endpoint, data, errorMessage) {
      try {
        const response = await apiClient.post(endpoint, data);
        return response.data;
      } catch (error) {
        this.errorMessage = errorMessage;
        console.error(error);
        throw error;
      }
    },
    async loadMatchDetails() {
      this.match = await this.fetchData(`/matches/${this.matchId}`, 'Failed to fetch match details!');
    },
    async loadPlayers() {
      this.players = await this.fetchData(`/matches/${this.matchId}/players`, 'Failed to fetch players!');
    },
    async loadHandsForPlayers() {
      if (this.match && this.match.current_round_id) {
        const data = await this.fetchData(`/rounds/${this.match.current_round_id}`, 'Failed to fetch hands!');
        const hands = data.hands;

        this.players.forEach((player) => {
          player.handSize = hands[player.user_id]?.size || 0;
        });

        this.match.stock_pile_size = data.stock_pile_size || 0;
      }
    },
    async loadMyHand() {
      if (this.match && this.match.current_round_id) {
        const data = await this.fetchData(`/rounds/${this.match.current_round_id}/my_hand`, 'Failed to fetch your hand!');
        this.myHand = data.cards;
      }
    },
    async loadCurrentTurn() {
      if (this.match && this.match.current_round_id) {
        const data = await this.fetchData(`/rounds/${this.match.current_round_id}/current_turn`, 'Failed to fetch current turn!');
        this.currentTurnUserId = data.user_id;
        this.turnId = data.turn_id;
      }
    },
    async handleStockPileClick() {
      if (this.isCurrentUserTurn && !this.loading) {
        this.loading = true;
        try {
          const response = await this.postData(`/turns/${this.turnId}/draw_from_stock_pile`, {}, 'Failed to draw from stock pile!');
          this.myHand.push(response.new_card);
          this.match.stock_pile_size -= 1;
        } catch (error) {
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
          await this.postData(`/matches/${this.matchId}/start`, {}, 'Failed to start match!');
          await this.loadMatchDetails();
        } catch (error) {
          console.error(error);
        } finally {
          this.loading = false;
        }
      }
    },
    clearErrorMessage() {
      this.errorMessage = '';
    },
    formatDateTime,
  },
  computed: {
    canStartMatch() {
      return this.players.length >= this.minPlayers && this.players.length <= this.maxPlayers && !this.match.start_time;
    },
    isCurrentUserTurn() {
      return this.currentTurnUserId === this.signedInUserId;
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

.players-list {
  list-style-type: none;
  padding: 0;
  width: 100%;
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
