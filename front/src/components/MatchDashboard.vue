<template>
  <div class="match-details">
    <h1>Match ID: {{ matchId }}</h1>
    <ErrorBox v-if="errorTitle" :title="errorTitle" :message="errorMessage" @close="clearErrorBox" />
    <LoadingIndicator :visible="loading" />
    <div v-if="match">
      <MatchTable
          :match="match"
          :players="players"
          :myHand="myHand"
          :signedInUserId="signedInUserId"
          :currentTurnUserId="currentTurnUserId"
          :loading="loading"
          @stock-pile-click="handleStockPileClick"
      />
      <button v-if="canStartMatch" @click="startMatch">Start Match</button>
    </div>
    <div v-else>
      <p>Loading match details...</p>
    </div>
  </div>
</template>

<script>
import matchService from '../services/matchService';
import { formatDateTime } from '../utils/dateFormatter';
import ErrorBox from './ErrorBox.vue';
import LoadingIndicator from './LoadingIndicator.vue';
import MatchTable from './MatchTable.vue';

export default {
  name: 'MatchDashboard',
  components: {
    ErrorBox,
    LoadingIndicator,
    MatchTable,
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
      errorTitle: '',
      errorMessage: ''
    };
  },
  async created() {
    await this.loadData([
      { method: this.loadMatchDetails, errorTitle: 'Failed to fetch match details!' },
      { method: this.loadPlayers, errorTitle: 'Failed to fetch players!' },
      { method: this.loadHandsForPlayers, errorTitle: 'Failed to fetch hands!' },
      { method: this.loadMyHand, errorTitle: 'Failed to fetch your hand!' },
      { method: this.loadCurrentTurn, errorTitle: 'Failed to fetch current turn!' },
    ]);
  },
  methods: {
    async loadData(tasks) {
      for (const { method, errorTitle } of tasks) {
        await this.handleApiCall(method, errorTitle);
      }
    },
    async handleApiCall(apiCall, errorTitle) {
      this.loading = true;
      try {
        await apiCall();
      } catch (error) {
        this.setErrorMessage(errorTitle, error.message);
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    async loadMatchDetails() {
      this.match = await matchService.getMatchDetails(this.matchId);
    },
    async loadPlayers() {
      this.players = await matchService.getPlayers(this.matchId);
    },
    async loadHandsForPlayers() {
      if (this.match && this.match.current_round_id) {
        const data = await matchService.getHandsForPlayers(this.match.current_round_id);
        const hands = data.hands;
        this.players.forEach(player => {
          player.handSize = hands[player.user_id]?.size || 0;
        });
        this.match.stock_pile_size = data.stock_pile_size || 0;
      }
    },
    async loadMyHand() {
      if (this.match && this.match.current_round_id) {
        const data = await matchService.getMyHand(this.match.current_round_id);
        this.myHand = data.cards;
      }
    },
    async loadCurrentTurn() {
      if (this.match && this.match.current_round_id) {
        const data = await matchService.getCurrentTurn(this.match.current_round_id);
        this.currentTurnUserId = data.user_id;
        this.turnId = data.turn_id;
      }
    },
    async handleStockPileClick() {
      if (this.isCurrentUserTurn && !this.loading) {
        await this.handleApiCall(
            async () => {
              const data = await matchService.drawFromStockPile(this.turnId);
              this.myHand.push(data.new_card);
              this.match.stock_pile_size -= 1;
            },
            'Failed to draw from stock pile!'
        );
      }
    },
    async startMatch() {
      if (!this.loading) {
        await this.handleApiCall(
            async () => {
              await matchService.startMatch(this.matchId);
              await this.loadMatchDetails();
            },
            'Failed to start match!'
        );
      }
    },
    setErrorMessage(title, message) {
      this.errorTitle = title;
      this.errorMessage = message;
    },
    clearErrorBox() {
      this.errorTitle = '';
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
