<template>
  <div class="match-details">
    <h1>Match ID: {{ matchId }}</h1>
    <ErrorBox v-if="errorTitle" :title="errorTitle" :message="errorMessage" @close="clearErrorBox" />
    <LoadingIndicator :visible="loading" />
    <MatchContent
        :match="match"
        :players="players"
        :myHand="myHand"
        :signedInUserId="signedInUserId"
        :currentTurnUserId="currentTurnUserId"
        :loading="loading"
        :canStartMatch="canStartMatch"
        @stock-pile-click="handleStockPileClick"
        :stockPileDisabled="!isCurrentUserTurn || loading || hasDrawAction"
        @start-match="startMatch"
    />
  </div>
</template>

<script>
import matchesService from '../services/matchesService';
import roundsService from "../services/roundsService";
import turnsService from "../services/turnsService";
import { setErrorMessage, clearErrorMessage } from '../utils/errorHandler';
import ErrorBox from './ErrorBox.vue';
import LoadingIndicator from './LoadingIndicator.vue';
import MatchContent from './MatchContent.vue';

export default {
  name: 'MatchDashboard',
  components: {
    ErrorBox,
    LoadingIndicator,
    MatchContent,
  },
  data() {
    return {
      matchId: this.$route.params.id,
      match: {
        create_time: '',
        created_by: null,
        current_round_id: null,
        end_time: null,
        match_id: null,
        start_time: null,
        stock_pile_size: 0,
      },
      players: [],
      myHand: [],
      currentTurnUserId: null,
      turnId: null,
      currentTurnActions: [],
      loading: true,
      errorTitle: '',
      errorMessage: '',
      signedInUserId: parseInt(localStorage.getItem('user_id'), 10),
      minPlayers: 2,
      maxPlayers: 4,
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
        setErrorMessage(this, errorTitle, error);
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    async loadMatchDetails() {
      this.match = await matchesService.getMatchDetails(this.matchId);
    },
    async loadPlayers() {
      this.players = await matchesService.getPlayers(this.matchId);
    },
    async loadHandsForPlayers() {
      if (this.match.current_round_id) {
        const data = await roundsService.getHandsForPlayers(this.match.current_round_id);
        const hands = data.hands;
        this.players.forEach(player => {
          player.handSize = hands[player.user_id]?.size || 0;
        });
        this.match.stock_pile_size = data.stock_pile_size || 0;
      }
    },
    async loadMyHand() {
      if (this.match.current_round_id) {
        const data = await roundsService.getMyHand(this.match.current_round_id);
        this.myHand = data.cards;
      }
    },
    async loadCurrentTurn() {
      if (this.match.current_round_id) {
        const data = await roundsService.getCurrentTurn(this.match.current_round_id);
        this.currentTurnUserId = data.user_id;
        this.turnId = data.turn_id;
        this.currentTurnActions = data.actions || [];
      }
    },
    async handleStockPileClick() {
      if (this.isCurrentUserTurn && !this.loading && !this.hasDrawAction) {
        await this.handleApiCall(
            async () => {
              const data = await turnsService.drawFromStockPile(this.turnId);
              this.myHand.push(data);
              this.match.stock_pile_size -= 1;
              // Add "draw" action to the currentTurnActions
              this.currentTurnActions.push({ type: 'draw' });
            },
            'Failed to draw from stock pile!'
        );
      }
    },
    async startMatch() {
      if (!this.loading) {
        await this.handleApiCall(
            async () => {
              await matchesService.startMatch(this.matchId);
              await this.loadMatchDetails();
            },
            'Failed to start match!'
        );
      }
    },
    clearErrorBox() {
      clearErrorMessage(this);
    },
  },
  computed: {
    canStartMatch() {
      return this.players.length >= this.minPlayers && this.players.length <= this.maxPlayers && !this.match.start_time;
    },
    isCurrentUserTurn() {
      return this.currentTurnUserId === this.signedInUserId;
    },
    hasDrawAction() {
      return this.currentTurnActions.some(action => action.action_type === 'draw');
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
