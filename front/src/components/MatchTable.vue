<template>
  <div class="match-table">
    <StockPile
        v-if="match && match.stock_pile_size !== undefined"
        :size="match.stock_pile_size"
        @click="handleStockPileClick"
        :disabled="stockPileDisabled"
    />
    <DiscardPile
        v-if="match && match.discard_pile"
        :visibleCards="match.discard_pile"
    />
    <button
        v-if="isCurrentUserTurn && !loading && hasDrawAction && hasOneSelectedCard"
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
import DiscardPile from './DiscardPile.vue';
import MatchPlayerList from './MatchPlayerList.vue';
import turnsService from "../services/turnsService";
import matchesService from '../services/matchesService';
import roundsService from "@/services/roundsService";

export default {
  name: 'MatchTable',
  components: {
    StockPile,
    DiscardPile,
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
      selectedCards: [],
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
    hasOneSelectedCard() {
      return this.selectedCards.length === 1;
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
        this.match.discard_pile = data.discard_pile || [];
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
      if (this.isCurrentUserTurn && !this.loading && this.hasDrawAction && this.hasOneSelectedCard) {
        this.$emit('loading', true);
        try {
          const selectedCard = this.selectedCards[0];
          await turnsService.discardCard(this.matchId, selectedCard.card_id);
          this.myHand = this.myHand.filter(card => card.card_id !== selectedCard.card_id);
          this.updateSelectedCards([]);
          this.match.discard_pile.push(selectedCard);
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
      this.selectedCards = selectedCards;
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
