<template>
  <div class="match-table">
    <StockPile
        v-if="match && match.stock_pile_size !== undefined"
        :size="match.stock_pile_size"
        @click="handleStockPileClick"
        :disabled="stockPileDisabled"
    />
    <button
        v-if="isCurrentUserTurn && !loading && hasDrawAction && selectedCard"
        @click="handleDiscardClick"
    >
      Discard
    </button>
    <MatchPlayerList
        :players="processedPlayers"
        :signedInUserId="signedInUserId"
        :currentTurnUserId="currentTurnUserId"
        @update:selectedCards="updateSelectedCards"
    />
  </div>
</template>

<script>
import StockPile from './StockPile.vue';
import MatchPlayerList from './MatchPlayerList.vue';
import turnsService from "../services/turnsService";
import matchesService from '../services/matchesService';
import roundsService from "@/services/roundsService";

export default {
  name: 'MatchTable',
  components: {
    StockPile,
    MatchPlayerList,
  },
  props: {
    matchId: {
      type: Number,
      required: true,
    },
    players: {
      type: Array,
      required: true,
    },
    signedInUserId: {
      type: Number,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    }
  },
  data() {
    return {
      match: null,
      myHand: [],
      currentTurnUserId: null,
      currentTurnActions: [],
      selectedCard: null,
    };
  },
  async created() {
    await this.loadAllData();
  },
  computed: {
    processedPlayers() {
      return this.players.map(player => {
        return {
          ...player,
          hand: player.user_id === this.signedInUserId ? this.myHand : [],
          hiddenCardCount: player.user_id !== this.signedInUserId ? player.handSize : 0,
          highlightPlayer: player.user_id === this.currentTurnUserId,
          selectable: this.isCurrentUserTurn,
        };
      });
    },
    isCurrentUserTurn() {
      return this.currentTurnUserId === this.signedInUserId;
    },
    hasDrawAction() {
      return this.currentTurnActions.some(action => action.action_type === 'draw');
    },
    stockPileDisabled() {
      return !this.isCurrentUserTurn || this.loading || this.hasDrawAction;
    }
  },
  methods: {
    async loadMatchDetails() {
      try {
        this.match = await matchesService.getMatchDetails(this.matchId);
      } catch (error) {
        this.$emit('error', 'Failed to fetch match details!', error);
      }
    },
    async loadCurrentTurn() {
      if (this.match.current_round_id) {
        const data = await roundsService.getCurrentTurn(this.match.current_round_id);
        this.currentTurnUserId = data.user_id;
        this.currentTurnActions = data.actions || [];
      }
    },
    async loadMyHand() {
      if (this.match.current_round_id) {
        try {
          const data = await roundsService.getMyHand(this.match.current_round_id);
          this.myHand = data.cards;
        } catch (error) {
          this.$emit('error', 'Failed to fetch your hand!', error);
        }
      }
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
    async handleStockPileClick() {
      if (this.isCurrentUserTurn && !this.loading && !this.hasDrawAction) {
        this.$emit('loading', true);
        try {
          const card = await turnsService.drawFromStockPile(this.matchId);
          this.myHand.push(card)
          this.match.stock_pile_size = this.match.stock_pile_size - 1;
          this.currentTurnActions.push({action_type: 'draw'});
        } catch (error) {
          this.$emit('error', 'Failed to draw from stock pile!', error);
        } finally {
          this.$emit('loading', false);
        }
      }
    },
    async handleDiscardClick() {
      if (this.isCurrentUserTurn && !this.loading && this.hasDrawAction && this.selectedCard) {
        this.$emit('loading', true);
        try {
          await turnsService.discardCard(this.matchId, this.selectedCard.card_id);
          this.myHand = this.myHand.filter(card => card.card_id !== this.selectedCard.card_id);
          this.selectedCard = null;
        } catch (error) {
          this.$emit('error', 'Failed to discard card!', error);
        } finally {
          this.$emit('loading', false);
        }
      }
    },
    async loadAllData() {
      await this.loadMatchDetails();
      await this.loadCurrentTurn();
      await this.loadMyHand();
      await this.loadHandsForPlayers();
    },
    updateSelectedCards(selectedCards) {
      this.selectedCard = selectedCards.length === 1 ? selectedCards[0] : null;
    }
  },
};
</script>

<style scoped>
.match-table {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
