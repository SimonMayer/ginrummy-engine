<template>
  <div class="match-table">
    <div class="non-self-players-container">
      <MatchPlayer
          v-for="player in nonSelfPlayers"
          :key="player.user_id"
          :ref="'player-' + player.user_id"
          :username="player.username"
          :hand="[]"
          :hiddenCardCount="player.hiddenCardCount"
          :highlightPlayer="player.highlightPlayer"
          :selectable="false"
          class="non-self-player"
      />
    </div>
    <div class="pile-container">
      <StockPile
          v-if="match && match.stock_pile_size !== undefined"
          :size="match.stock_pile_size"
          @click="handleStockPileClick"
          :disabled="stockPileDisabled"
      />
      <DiscardPile
          v-if="match && match.discard_pile"
          :visibleCards="match.discard_pile"
          @top-card-clicked="handleDiscardPileClick"
      />
    </div>
    <div class="buttons-container">
      <button @click="handleDiscardClick" :disabled="isDiscardButtonDisabled()">
        Discard
      </button>
    </div>
    <div class="self-player-container">
      <MatchPlayer
          v-if="selfPlayer"
          :key="selfPlayer.user_id"
          :ref="'player-self'"
          :username="selfPlayer.username"
          :hand="myHand"
          :hiddenCardCount="0"
          :highlightPlayer="selfPlayer.highlightPlayer"
          :selectable="isCurrentUserTurn"
          class="self-player"
      />
    </div>
  </div>
</template>

<script>
import StockPile from '@/components/StockPile.vue';
import DiscardPile from '@/components/DiscardPile.vue';
import MatchPlayer from '@/components/MatchPlayer.vue';
import turnsService from '@/services/turnsService';
import matchesService from '@/services/matchesService';
import roundsService from '@/services/roundsService';
import SSEService from '@/services/sseService';

export default {
  name: 'MatchTable',
  components: {
    StockPile,
    DiscardPile,
    MatchPlayer,
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
      sseService: null,
      currentTurnId: null,
      latestActionId: null,
    };
  },
  async created() {
    await this.loadAllData();
  },
  beforeUnmount() {
    this.cleanupSSE();
  },
  computed: {
    selfPlayer() {
      const player = this.players.find(player => player.user_id === this.signedInUserId);
      if (player) {
        return {
          ...player,
          highlightPlayer: player.user_id === this.currentTurnUserId,
        };
      }
      return null;
    },
    nonSelfPlayers() {
      const selfIndex = this.players.findIndex(player => player.user_id === this.signedInUserId);
      if (selfIndex === -1) {
        // If self player is not found, return the original array processed as usual
        return this.players.map(this.transformPlayer);
      }

      const beforeSelf = this.players.slice(0, selfIndex);
      const afterSelf = this.players.slice(selfIndex + 1);

      const reorderedPlayers = [...afterSelf, ...beforeSelf];

      return reorderedPlayers.map(this.transformPlayer);
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
    hasOneSelectedCard() {
      return this.getSelectedCardCount() === 1;
    },
    isDiscardButtonDisabled() {
      const signedInPlayer = this.$refs['player-self'];
      if (signedInPlayer) {
        signedInPlayer.hand; // causes a refresh — otherwise button seems to remain enabled
      }

      return !this.isCurrentUserTurn || this.loading || !this.hasDrawAction || !this.hasOneSelectedCard();
    },
    cleanupSSE() {
      if (this.sseService) {
        this.sseService.disconnect();
      }
    },
    transformPlayer(player) {
      return {
        ...player,
        hiddenCardCount: player.handSize,
        highlightPlayer: player.user_id === this.currentTurnUserId,
      };
    },
    getSelectedCards() {
      const signedInPlayer = this.$refs['player-self'];
      if (!signedInPlayer) {
        return [];
      }

      return signedInPlayer.getSelectedCards();
    },
    getSelectedCardCount() {
      return this.getSelectedCards().length;
    },
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
        this.currentTurnId = data.turn_id;
        this.latestActionId = data.latest_action_id;
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
          let card;
          if (this.match.stock_pile_size > 0) {
            card = await turnsService.drawFromStockPile(this.matchId);
            this.match.stock_pile_size -= 1;
          } else {
            card = await turnsService.drawFromEmptyStockPile(this.matchId);
          }
          this.myHand.push(card);
        } catch (error) {
          this.$emit('error', 'Failed to draw from stock pile!', error);
        } finally {
          this.$emit('loading', false);
        }
      }
    },
    async handleDiscardPileClick() {
      if (this.isCurrentUserTurn && !this.loading && !this.hasDrawAction && this.match.discard_pile.length > 0) {
        this.$emit('loading', true);
        try {
          const card = await turnsService.drawFromDiscardPile(this.matchId);
          this.myHand.push(card);
          this.match.discard_pile.pop();
        } catch (error) {
          this.$emit('error', 'Failed to draw from discard pile!', error);
        } finally {
          this.$emit('loading', false);
        }
      }
    },
    async handleDiscardClick() {
      if (this.isCurrentUserTurn && !this.loading && this.hasDrawAction && this.hasOneSelectedCard()) {
        this.$emit('loading', true);
        try {
          const selectedCard = this.getSelectedCards()[0];
          const cardId = selectedCard.cardData.card_id;

          await turnsService.discardCard(this.matchId, cardId);
          this.myHand = this.myHand.filter(card => card.card_id !== cardId);
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
      this.initializeSSE();
    },
    initializeSSE() {
      const latestActionId = this.latestActionId === null ? '' : this.latestActionId;
      const endpoint = `/matches/${this.matchId}/events?latest_action_id=${latestActionId}`;

      try {
        this.sseService = new SSEService(endpoint);

        this.sseService.connect(
            () => {
              this.loadCurrentTurn();
              this.loadHandsForPlayers();
            },
            (error) => {
              console.error('SSE error:', error);
            }
        );
      } catch (error) {
        console.error('Failed to initialize SSE:', error);
      }
    }
  },
};
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';

.match-table {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: var(--base-padding);
  gap: var(--base-margin);

  .pile-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--base-margin);
  }

  .buttons-container {
    display: flex;
    gap: var(--base-margin);
    justify-content: center;
    width: 100%;
  }

  .non-self-players-container {
    display: flex;
    justify-content: space-between;
    width: 100%;
  }

  .self-player-container {
    display: flex;
    justify-content: center;
    width: 100%;
  }
}
</style>
