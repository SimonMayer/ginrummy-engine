<template>
  <div class="match-table" v-if="match && match.discard_pile">
    <div class="game-section full-width">
      <div class="non-self-players-container">
        <NonSelfMatchPlayer
            v-for="player in nonSelfPlayers"
            :key="player.user_id"
            :ref="'player-' + player.user_id"
            :username="player.username"
            :score="player.score"
            :hiddenCardCount="player.hiddenCardCount"
            :highlightPlayer="player.highlightPlayer"
            class="non-self-player"
        />
      </div>
    </div>
    <div class="game-section row">
      <div class="game-column pile-container">
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
            :disabled="discardPileDisabled"
        />
      </div>
      <div class="game-column">
        <div class="melds-container">
          <PlayedMeld
              v-for="meld in allMelds"
              :key="meld.meld_id"
              :id="meld.meld_id"
              :type="meld.meld_type"
              :cards="meld.cards"
              :selected="selectedMeldId === meld.meld_id"
              :selectable="isMeldSelectable"
              @select:meld="handleMeldClick(meld.meld_id)"
          />
        </div>
        <div class="buttons-container">
          <button @click="handlePlaySetClick" :disabled="playSetButtonDisabled">
            Play set
          </button>
          <button @click="handlePlayRunClick" :disabled="playRunButtonDisabled">
            Play run
          </button>
          <button @click="handleExtendMeldClick" :disabled="extendMeldButtonDisabled">
            Extend meld
          </button>
          <button @click="handleDiscardClick" :disabled="discardButtonDisabled">
            Discard
          </button>
        </div>
        <div class="self-player-container">
          <SelfMatchPlayer
              v-if="selfPlayer"
              :key="selfPlayer.user_id"
              :ref="'player-self'"
              :username="selfPlayer.username"
              :score="selfPlayer.score"
              :hand="myHand"
              :highlightPlayer="selfPlayer.highlightPlayer"
              :selectable="isHandSelectable"
              class="self-player"
              @update:selected="forceRefresh()"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import configService from "@/services/configService";
import PlayedMeld from '@/components/PlayedMeld.vue';
import StockPile from '@/components/StockPile.vue';
import DiscardPile from '@/components/DiscardPile.vue';
import SelfMatchPlayer from '@/components/SelfMatchPlayer.vue';
import NonSelfMatchPlayer from '@/components/NonSelfMatchPlayer.vue';
import turnsService from '@/services/turnsService';
import matchesService from '@/services/matchesService';
import roundsService from '@/services/roundsService';
import SSEService from '@/services/sseService';

export default {
  name: 'MatchTable',
  components: {
    PlayedMeld,
    StockPile,
    DiscardPile,
    SelfMatchPlayer,
    NonSelfMatchPlayer
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
      refreshValues: 0,
      allowMeldsFromRotation: null,
      minimumMeldSize: null,
      runOrders: [],
      match: null,
      myHand: [],
      rotationNumber: null,
      currentTurnUserId: null,
      currentTurnActions: [],
      sseService: null,
      currentTurnId: null,
      latestActionId: null,
      selectedMeld: null,
    };
  },
  async created() {
    this.$emit('loading', true);
    await this.loadConfig();
    await this.loadAllData();
    this.$emit('loading', false);
  },
  beforeUnmount() {
    this.cleanupSSE();
  },
  computed: {
    selfPlayer() {
      const player = this.players.find(player => player.user_id === this.signedInUserId);
      if (player) {
        return this.transformPlayer(player);
      }
      return null;
    },
    nonSelfPlayers() {
      const selfIndex = this.players.findIndex(player => player.user_id === this.signedInUserId);
      if (selfIndex === -1) {
        return this.players.map(this.transformNonSelfPlayer);
      }

      const beforeSelf = this.players.slice(0, selfIndex);
      const afterSelf = this.players.slice(selfIndex + 1);

      return [...afterSelf, ...beforeSelf].map(this.transformNonSelfPlayer);
    },
    allMelds() {
      return this.players.reduce((allMelds, player) => {
        return allMelds.concat(player.melds || []);
      }, []);
    },
    selectedMeldId() {
      return this.selectedMeld ? this.selectedMeld.meld_id : null;
    },
    isCurrentUserTurn() {
      return this.currentTurnUserId === this.signedInUserId;
    },
    hasDrawAction() {
      return this.currentTurnActions.some(action => action.action_type === 'draw');
    },
    isHandSelectable() {
      return this.isCurrentUserTurn && this.hasDrawAction;
    },
    isMeldSelectable() {
      const selfPlayer = this.players.find(player => player.user_id === this.signedInUserId);
      return this.isCurrentUserTurn && this.hasDrawAction && selfPlayer && selfPlayer.melds && selfPlayer.melds.length > 0;
    },
    stockPileDisabled() {
      return !this.isCurrentUserTurn || this.loading || this.hasDrawAction;
    },
    discardPileDisabled() {
      return !this.isCurrentUserTurn || this.loading || this.hasDrawAction;
    },
    discardButtonDisabled() {
      this.refreshValues; // forces a recompute when refreshValues is changed
      return !this.isCurrentUserTurn || this.loading || !this.hasDrawAction || this.selectedMeld || !this.hasOneHandCardSelected();
    },
    playSetButtonDisabled() {
      this.refreshValues; // forces a recompute when refreshValues is changed
      const selectedHandCards = this.getSelectedHandCards();
      const allHandCardsSelected = selectedHandCards.length === this.myHand.length;
      const allSameRank = selectedHandCards.every(card => card.cardData.rank === selectedHandCards[0].cardData.rank);

      return !this.isCurrentUserTurn ||
          this.loading ||
          !this.hasDrawAction ||
          this.selectedMeld ||
          !(selectedHandCards.length >= this.minimumMeldSize) ||
          !allSameRank ||
          allHandCardsSelected;
    },
    playRunButtonDisabled() {
      this.refreshValues; // forces a recompute when refreshValues is changed
      const selectedHandCards = this.getSelectedHandCards();
      const allHandCardsSelected = selectedHandCards.length === this.myHand.length;
      const allSameSuit = selectedHandCards.every(card => card.cardData.suit === selectedHandCards[0].cardData.suit);
      const isValidRun = this.doSelectedHandCardsMakeValidRun();

      return !this.isCurrentUserTurn ||
          this.loading ||
          !this.hasDrawAction ||
          this.selectedMeld ||
          !(selectedHandCards.length >= this.minimumMeldSize) ||
          !allSameSuit ||
          allHandCardsSelected ||
          !isValidRun;
    },
    extendMeldButtonDisabled() {
      this.refreshValues; // forces a recompute when refreshValues is changed
      return !this.isCurrentUserTurn ||
          this.loading ||
          !this.hasDrawAction ||
          !this.selectedMeld ||
          this.getSelectedHandCards().length === 0 ||
          this.getSelectedHandCards().length === this.myHand.length ||
          !this.isValidMeldExtension();
    },
    playerScores() {
      const scores = {};

      this.allMelds.forEach(meld => {
        meld.cards.forEach(card => {
          if (scores[card.user_id]) {
            scores[card.user_id] += card.point_value;
          } else {
            scores[card.user_id] = card.point_value;
          }
        });
      });

      return this.players.map(player => {
        return { user_id: player.user_id, score: scores[player.user_id] || 0 };
      });
    }
  },
  methods: {
    hasOneHandCardSelected() {
      return this.getSelectedHandCardCount() === 1;
    },
    forceRefresh() {
      // forces refresh of computed values
      this.refreshValues++;
    },
    doSelectedHandCardsMakeValidRun() {
      const selectedHandCards = this.getSelectedHandCards();
      const cardRanks = selectedHandCards.map(card => card.cardData.rank);

      return this.runOrders.some(order => {
        const indices = cardRanks.map(rank => order.indexOf(rank)).sort((a, b) => a - b);
        return indices.every((index, i) => i === 0 || index === indices[i - 1] + 1);
      });
    },
    isValidMeldExtension() {
      const selectedHandCards = this.getSelectedHandCards();
      const noHandCardsSelected = selectedHandCards.length === 0;
      const allHandCardsSelected = selectedHandCards.length === this.myHand.length;

      if (!this.selectedMeld || noHandCardsSelected || allHandCardsSelected) return false;

      const meldCards = this.selectedMeld.cards.map(card => ({
        rank: card.rank,
        suit: card.suit
      }));
      const processedSelectedHandCards = selectedHandCards.map(card => card.cardData);
      const allCards = [...meldCards, ...processedSelectedHandCards];

      const allSameRank = allCards.every(card => card.rank === allCards[0].rank);
      const allSameSuit = allCards.every(card => card.suit === allCards[0].suit);
      const isValidRun = this.runOrders.some(order => {
        const ranks = allCards.map(card => card.rank);
        const indices = ranks.map(rank => order.indexOf(rank)).sort((a, b) => a - b);
        return indices.every((index, i) => i === 0 || index === indices[i - 1] + 1);
      });

      return allSameRank || (allSameSuit && isValidRun);
    },
    cleanupSSE() {
      if (this.sseService) {
        this.sseService.disconnect();
      }
    },
    transformPlayer(player) {
      const playerScore = this.playerScores.find(score => score.user_id === player.user_id);
      return {
        ...player,
        highlightPlayer: player.user_id === this.currentTurnUserId,
        score: playerScore ? playerScore.score : 0,
      };
    },
    transformNonSelfPlayer(player) {
      return {
        ...this.transformPlayer(player),
        hiddenCardCount: player.handSize,
      };
    },
    getSelectedHandCards() {
      const signedInPlayer = this.$refs['player-self'];
      if (!signedInPlayer) {
        return [];
      }

      return signedInPlayer.getSelectedCards();
    },
    getSelectedHandCardCount() {
      return this.getSelectedHandCards().length;
    },
    handleMeldClick(meldId) {
      const meld = this.allMelds.find(meld => meld.meld_id === meldId);
      if (!meld || (this.selectedMeldId === meldId)) {
        this.selectedMeld = null;
      } else {
        this.selectedMeld = meld;
      }
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
        this.rotationNumber = data.rotation_number;
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
    async loadRoundDataForPlayers() {
      if (this.match.current_round_id) {
        const data = await roundsService.getRoundDataForPlayers(this.match.current_round_id);
        const players = data.players;
        this.players.forEach(player => {
          const playerData = players.find(p => p.user_id === player.user_id);
          player.handSize = playerData ? playerData.hand.size : 0;
          player.melds = playerData.melds;
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
      if (this.isCurrentUserTurn && !this.loading && this.hasDrawAction && this.hasOneHandCardSelected()) {
        this.$emit('loading', true);
        try {
          const selectedCard = this.getSelectedHandCards()[0];
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
    async handlePlaySetClick() {
      if (this.getSelectedHandCardCount() >= this.minimumMeldSize && this.rotationNumber >= this.allowMeldsFromRotation) {
        this.$emit('loading', true);
        try {
          const selectedHandCards = this.getSelectedHandCards();
          const cardIds = selectedHandCards.map(card => card.cardData.card_id);
          await turnsService.playMeld(this.matchId, cardIds, 'set');
          this.myHand = this.myHand.filter(card => !cardIds.includes(card.card_id));
        } catch (error) {
          this.$emit('error', 'Failed to play meld!', error);
        } finally {
          this.$emit('loading', false);
        }
      }
    },
    async handlePlayRunClick() {
      if (this.getSelectedHandCardCount() >= this.minimumMeldSize && this.rotationNumber >= this.allowMeldsFromRotation) {
        this.$emit('loading', true);
        try {
          const selectedHandCards = this.getSelectedHandCards();
          const cardIds = selectedHandCards.map(card => card.cardData.card_id);
          await turnsService.playMeld(this.matchId, cardIds, 'run');
          this.myHand = this.myHand.filter(card => !cardIds.includes(card.card_id));
        } catch (error) {
          this.$emit('error', 'Failed to play meld!', error);
        } finally {
          this.$emit('loading', false);
        }
      }
    },
    async handleExtendMeldClick() {
      if (this.isCurrentUserTurn && !this.loading && this.hasDrawAction && this.selectedMeld && this.getSelectedHandCards().length > 0) {
        this.$emit('loading', true);
        try {
          const selectedHandCards = this.getSelectedHandCards();
          const cardIds = selectedHandCards.map(card => card.cardData.card_id);
          await turnsService.extendMeld(this.matchId, this.selectedMeld.meld_id, cardIds);
          this.myHand = this.myHand.filter(card => !cardIds.includes(card.card_id));
        } catch (error) {
          this.$emit('error', 'Failed to extend meld!', error);
        } finally {
          this.$emit('loading', false);
          this.forceRefresh();
        }
      }
    },
    async loadConfig() {
      try {
        const config = await configService.getGameConfig();
        this.allowMeldsFromRotation = config.allowMeldsFromRotation;
        this.minimumMeldSize = config.minimumMeldSize;
        this.runOrders = config.runOrders;
      } catch (error) {
        this.handleError('Failed to fetch game configuration!', error);
      }
    },
    async loadAllData() {
      await this.loadMatchDetails();
      await this.loadCurrentTurn();
      await this.loadMyHand();
      await this.loadRoundDataForPlayers();
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
              this.loadRoundDataForPlayers();
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
  align-items: stretch;
  gap: var(--base-margin);

  .game-section{
    &.full-width {
      flex-basis: 100%;
      padding: 10px;
      text-align: center;
    }

    &.row {
      display: flex;
      width: 100%;

      .column {
        flex: 1;
        padding: 10px;
        text-align: center;
      }
    }
  }

  .pile-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--base-margin);
    height: 100%;
    position: relative;

    .stock-pile-container, .discard-pile {
      transform-origin: top left;
      transform: rotate(90deg) translateY(calc(var(--card-height) * -1));
    }

    .discard-pile {
      position: absolute;
      top: calc((var(--card-width) * 1.5) + var(--base-margin));
      left: calc(2 * var(--base-margin));
    }
  }

  .game-column:not(.pile-container) {
    flex: 1; // Take up remaining space
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: var(--base-margin);
  }

  .melds-container {
    display: flex;
    gap: var(--base-margin);
    justify-content: center;
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
