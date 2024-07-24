<template>
  <div class="match-table" v-if="match">
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
            :ref="'discard-pile'"
            :visibleCards="match.discard_pile"
            :selectableCards="getSelectableDiscardPileCards()"
            @update:selected="forceRefresh()"
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
              :runOrders="runOrders"
              @select:meld="handleMeldClick(meld.meld_id)"
          />
        </div>
        <div v-if="!currentRoundId" class="buttons-container">
          <button @click="handleStartNewRound">Start new round</button>
        </div>
        <div v-if="currentRoundId" class="buttons-container">
          <button @click="handleDrawOneFromDiscardPileClick" :disabled="drawOneFromDiscardPileButtonDisabled">
            Draw one from discard pile
          </button>
          <button @click="handleDrawMultipleFromDiscardPileClick" :disabled="drawMultipleFromDiscardPileButtonDisabled">
            Draw multiple from discard pile
          </button>
          <button @click="handlePlaySetClick" :disabled="playSetButtonDisabled">Play set</button>
          <button @click="handlePlayRunClick" :disabled="playRunButtonDisabled">Play run</button>
          <button @click="handleExtendMeldClick" :disabled="extendMeldButtonDisabled">Extend meld</button>
          <button @click="handleDiscardClick" :disabled="discardButtonDisabled">Discard</button>
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
  components: { PlayedMeld, StockPile, DiscardPile, SelfMatchPlayer, NonSelfMatchPlayer },
  props: {
    matchId: { type: Number, required: true },
    players: { type: Array, required: true },
    signedInUserId: { type: Number, required: true },
    loading: { type: Boolean, required: true }
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
      currentRoundId: null,
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
      return player ? this.transformPlayer(player) : null;
    },
    nonSelfPlayers() {
      const selfIndex = this.players.findIndex(player => player.user_id === this.signedInUserId);
      if (selfIndex === -1) {
        return this.players.map(this.transformNonSelfPlayer);
      }
      return [...this.players.slice(selfIndex + 1), ...this.players.slice(0, selfIndex)].map(this.transformNonSelfPlayer);
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
    hasPlayedMeld() {
      const selfPlayer = this.players.find(player => player.user_id === this.signedInUserId);
      return selfPlayer && selfPlayer.melds && selfPlayer.melds.length > 0;
    },
    isHandSelectable() {
      return this.canDrawMultiple() || (this.canAct() && this.hasDrawAction);
    },
    isMeldSelectable() {
      return this.canAct() && this.hasPlayedMeld;
    },
    stockPileDisabled() {
      return !this.canDrawFromStockPile()
    },
    discardButtonDisabled() {
      this.refreshValues; // forces a recompute when refreshValues is changed
      return !this.canDiscard();
    },
    playSetButtonDisabled() {
      this.refreshValues; // forces a recompute when refreshValues is changed
      return !this.canPlaySet();
    },
    playRunButtonDisabled() {
      this.refreshValues; // forces a recompute when refreshValues is changed
      return !this.canPlayRun();
    },
    extendMeldButtonDisabled() {
      this.refreshValues; // forces a recompute when refreshValues is changed
      return !this.canExtendMeld();
    },
    drawOneFromDiscardPileButtonDisabled() {
      this.refreshValues; // forces a recompute when refreshValues is changed
      return !this.canDrawOneFromDiscardPile();
    },
    drawMultipleFromDiscardPileButtonDisabled() {
      this.refreshValues; // forces a recompute when refreshValues is changed
      return !this.canDrawMultipleFromDiscardPile();
    }
  },
  methods: {
    hasNoHandCardsSelected() {
      return this.getSelectedHandCardCount() === 0;
    },
    hasOneHandCardSelected() {
      return this.getSelectedHandCardCount() === 1;
    },
    hasAllHandCardsSelected() {
      return this.getSelectedHandCardCount() === this.myHand.length;
    },
    isCardAvailableForHandAfterDrawMultipleAction() {
      const selectedCardCount = this.getSelectedHandCardCount() + this.getSelectedDiscardPileCardCount();
      return selectedCardCount < (this.myHand.length + this.getDiscardPileCardsStartingFromBottomSelectedCard().length);
    },
    hasNoDiscardPileCardsSelected() {
      return this.getSelectedDiscardPileCardCount() === 0;
    },
    hasOneDiscardPileCardSelected() {
      return this.getSelectedDiscardPileCardCount() === 1;
    },
    isOnlyTopDiscardPileCardSelected() {
      return this.hasOneDiscardPileCardSelected() && this.getTopDiscardPileCard().card_id === this.getSelectedDiscardPileCards()[0]?.card_id;
    },
    isAnyDiscardPileCardSelected() {
      return this.getSelectedDiscardPileCardCount() > 0;
    },
    isBottomSelectedDiscardPileCardAtTheTop() {
      return this.getBottomSelectedCardInDiscardPile().card_id === this.getTopDiscardPileCard().card_id;
    },
    areAllCardsOfSameRank(cards) {
      return cards.every(card => card.rank === cards[0].rank);
    },
    areAllCardsOfSameSuit(cards) {
      return cards.every(card => card.suit === cards[0].suit);
    },
    doCardsMakeValidRun(cards) {
      return this.areAllCardsOfSameSuit(cards) && this.runOrders.some(order => {
        const ranks = cards.map(card => card.rank);
        const indices = ranks.map(rank => order.indexOf(rank)).sort((a, b) => a - b);
        return indices.every((index, i) => i === 0 || index === indices[i - 1] + 1);
      });
    },
    doSelectedHandCardsMakeValidRun() {
      return this.doCardsMakeValidRun(this.getSelectedHandCards());
    },
    isEnoughCardsForMeld(cards) {
      return cards.length >= this.minimumMeldSize;
    },
    isRotationThatAllowsMelds(){
      return this.rotationNumber >= this.allowMeldsFromRotation;
    },
    canAct() {
      return this.isCurrentUserTurn && !this.loading;
    },
    canDraw() {
      return this.canAct() && !this.hasDrawAction;
    },
    canDrawOne() {
      return this.canDraw() && this.hasNoHandCardsSelected() && !this.selectedMeld;
    },
    canDrawMultiple() {
      return this.canDraw() && this.hasPlayedMeld;
    },
    canDrawFromStockPile() {
      return this.canDrawOne() && this.hasNoDiscardPileCardsSelected();
    },
    canDrawOneFromDiscardPile() {
      return this.canDrawOne() && this.isOnlyTopDiscardPileCardSelected();
    },
    canDrawMultipleFromDiscardPile() {
      return this.canDrawMultiple() &&
          this.isRotationThatAllowsMelds() &&
          this.isAnyDiscardPileCardSelected() &&
          !this.isBottomSelectedDiscardPileCardAtTheTop() &&
          this.isCardAvailableForHandAfterDrawMultipleAction() &&
          this.doSelectedCardsFormValidMeld();
    },
    canPlayMeld() {
      return this.canAct() &&
          this.hasDrawAction &&
          !this.selectedMeld &&
          this.isRotationThatAllowsMelds() &&
          this.isEnoughCardsForMeld(this.getSelectedHandCards()) &&
          !this.hasAllHandCardsSelected();
    },
    canPlayRun() {
      return this.canPlayMeld() && this.doSelectedHandCardsMakeValidRun();
    },
    canPlaySet() {
      return this.canPlayMeld() && this.areAllCardsOfSameRank(this.getSelectedHandCards());
    },
    canExtendMeld() {
      return this.canAct() &&
          this.hasDrawAction &&
          this.hasPlayedMeld &&
          this.selectedMeld &&
          this.isRotationThatAllowsMelds() &&
          !this.hasNoHandCardsSelected() &&
          !this.hasAllHandCardsSelected() &&
          this.isValidMeldExtension();
    },
    canDiscard() {
      return this.canAct() && this.hasDrawAction && !this.selectedMeld && this.hasOneHandCardSelected();
    },
    forceRefresh() {
      // forces refresh of computed values
      this.refreshValues++;
    },
    doSelectedCardsFormValidMeld() {
      const allSelectedCards = this.getAllSelectedCards();
      return this.isEnoughCardsForMeld(allSelectedCards) &&
          (this.areAllCardsOfSameRank(allSelectedCards) || this.doCardsMakeValidRun(allSelectedCards));
    },
    isValidMeldExtension() {
      if (!this.selectedMeld || this.hasNoHandCardsSelected() || this.hasAllHandCardsSelected()) {
        return false;
      }
      const allCards = [...this.getSelectedMeldCards(), ...this.getSelectedHandCards()];
      return this.areAllCardsOfSameRank(allCards) || this.doCardsMakeValidRun(allCards);
    },
    cleanupSSE() {
      if (this.sseService) {
        this.sseService.disconnect();
      }
    },
    transformPlayer(player) {
      return {
        ...player,
        highlightPlayer: player.user_id === this.currentTurnUserId
      };
    },
    transformNonSelfPlayer(player) {
      return {
        ...this.transformPlayer(player),
        hiddenCardCount: player.handSize,
      };
    },
    getTopDiscardPileCard() {
      const discardPile = this.match.discard_pile;
      return discardPile ? discardPile[discardPile.length - 1] : null;
    },
    getDiscardPileCardsStartingFromBottomSelectedCard() {
      const discardPile = this.match.discard_pile;
      const bottomCardIndex = discardPile.findIndex(card => card.card_id === this.getBottomSelectedCardInDiscardPile().card_id);
      return discardPile.slice(bottomCardIndex);
    },
    getSelectableDiscardPileCards() {
      return this.canDrawMultiple()
          ? this.match.discard_pile
          : this.canDrawOne() ? [this.getTopDiscardPileCard()] : [];
    },
    getSelectedCards(refName) {
      return this.$refs[refName] ? this.$refs[refName].getSelectedCards() : [];
    },
    getAllSelectedCards() {
      return [...this.getSelectedMeldCards(), ...this.getSelectedHandCards(), ...this.getSelectedDiscardPileCards()];
    },
    getSelectedMeldCards() {
      return this.selectedMeld ? this.selectedMeld.cards : [];
    },
    getSelectedDiscardPileCards() {
      return this.getSelectedCards('discard-pile').map(card => card.cardData);
    },
    getSelectedDiscardPileCardCount() {
      return this.getSelectedDiscardPileCards().length;
    },
    getBottomSelectedCardInDiscardPile() {
      const selectedDiscardPileCards = this.getSelectedDiscardPileCards();
      return selectedDiscardPileCards ? selectedDiscardPileCards[0] : null
    },
    getSelectedHandCards() {
      return this.getSelectedCards('player-self').map(card => card.cardData);
    },
    getSelectedHandCardCount() {
      return this.getSelectedHandCards().length;
    },
    unselectCardsByRef(refName) {
      const ref = this.$refs[refName];
      if (ref) {
        ref.unselectAllCards();
      }
    },
    unselectHandCards() {
      this.unselectCardsByRef('player-self');
    },
    unselectDiscardPileCards() {
      this.unselectCardsByRef('discard-pile');
    },
    unselectMeld() {
      this.selectedMeld = null;
    },
    handleMeldClick(meldId) {
      const meld = this.allMelds.find(meld => meld.meld_id === meldId);
      this.selectedMeld = !meld || (this.selectedMeldId === meldId) ? null : meld;
    },
    async loadMatchDetails() {
      try {
        const data = await matchesService.getMatchDetails(this.matchId);
        this.match = data;
        this.currentRoundId = data.current_round_id;
      } catch (error) {
        this.$emit('error', 'Failed to fetch match details!', error);
      }
    },
    async loadCurrentTurn() {
      if (this.currentRoundId) {
        const data = await roundsService.getCurrentTurn(this.currentRoundId);
        this.currentTurnUserId = data.user_id;
        this.currentTurnActions = data.actions || [];
        this.currentTurnId = data.turn_id;
        this.latestActionId = data.latest_action_id;
        this.rotationNumber = data.rotation_number;
      }
    },
    async loadMyHand() {
      if (this.currentRoundId) {
        try {
          const data = await roundsService.getMyHand(this.currentRoundId);
          this.myHand = data.cards;
        } catch (error) {
          this.$emit('error', 'Failed to fetch your hand!', error);
        }
      }
    },
    async loadCurrentRoundDataForPlayers() {
      if (this.currentRoundId) {
        this.loadRoundDataForPlayers(this.currentRoundId);
      }
    },
    async loadRoundDataForPlayers(roundId) {
        const data = await roundsService.getRoundDataForPlayers(roundId);
        const players = data.players;
        this.players.forEach(player => {
          const playerData = players.find(p => p.user_id === player.user_id);
          player.handSize = playerData ? playerData.hand.size : 0;
          player.melds = playerData.melds;
          player.score = playerData.score.total_score;
        });
        this.match.stock_pile_size = data.stock_pile_size || 0;
        this.match.discard_pile = data.discard_pile || [];
    },
    async performAction(action, errorMessage) {
      this.$emit('loading', true);
      try {
        await action();
      } catch (error) {
        this.$emit('error', errorMessage, error);
      } finally {
        this.$emit('loading', false);
        this.forceRefresh();
      }
    },
    async handleStockPileClick() {
      await this.handleDrawOneFromPileClick('stock');
    },
    async handleDrawOneFromDiscardPileClick() {
      await this.handleDrawOneFromPileClick('discard');
    },
    async handleDrawOneFromPileClick(pileType) {
      if ((pileType === 'discard' && !this.canDrawOneFromDiscardPile()) || !this.canDraw()) {
        return;
      }
      await this.performAction(async () => {
        let card;
        if (pileType === 'stock') {
          card = this.match.stock_pile_size > 0
              ? await turnsService.drawFromStockPile(this.matchId)
              : await turnsService.drawFromEmptyStockPile(this.matchId);
        } else if (pileType === 'discard') {
          card = await turnsService.drawOneFromDiscardPile(this.matchId);
          this.match.discard_pile.pop();
        }
        this.unselectDiscardPileCards();
        this.myHand.push(card);
      }, `Failed to draw from ${pileType} pile!`);
    },
    async handleDrawMultipleFromDiscardPileClick() {
      if (!this.canDrawMultipleFromDiscardPile()) {
        return;
      }
      await this.performAction(async () => {
        const handCardIds = this.getSelectedHandCards().map(card => card.card_id);
        const discardPileCardIds = this.getSelectedDiscardPileCards().map(card => card.card_id);
        const newHandCards = await turnsService.drawMultipleFromDiscardPile(
            this.matchId,
            discardPileCardIds,
            handCardIds,
            this.selectedMeldId
        );
        this.unselectDiscardPileCards();
        this.unselectHandCards();
        this.unselectMeld();
        this.myHand = this.myHand.filter(handCard => !handCardIds.includes(handCard.card_id));
        newHandCards.forEach(newHandCard => {
          this.myHand.push(newHandCard);
        });
      }, `Failed to draw multiple from discard pile!`);
    },
    async handleDiscardClick() {
      if(!this.canDiscard()){
        return;
      }
      await this.performAction(async () => {
        const cardId = this.getSelectedHandCards()[0].card_id;
        await turnsService.discardCard(this.matchId, cardId);
        this.unselectHandCards();
        this.myHand = this.myHand.filter(card => card.card_id !== cardId);
      }, 'Failed to discard card!');
    },
    async handlePlayMeldClick(meldType) {
      if(!this.canPlaySet() && !this.canPlayRun()) {
        return;
      }
      await this.performAction(async () => {
        const cardIds = this.getSelectedHandCards().map(card => card.card_id);
        await turnsService.playMeld(this.matchId, cardIds, meldType);
        this.myHand = this.myHand.filter(card => !cardIds.includes(card.card_id));
      }, `Failed to play meld!`);
    },
    async handlePlaySetClick() {
      await this.handlePlayMeldClick('set');
    },
    async handlePlayRunClick() {
      await this.handlePlayMeldClick('run');
    },
    async handleExtendMeldClick() {
      if(!this.canExtendMeld()) {
        return;
      }
      await this.performAction(async () => {
        const cardIds = this.getSelectedHandCards().map(card => card.card_id);
        await turnsService.extendMeld(this.matchId, this.selectedMeldId, cardIds);
        this.unselectMeld();
        this.myHand = this.myHand.filter(card => !cardIds.includes(card.card_id));
      }, 'Failed to extend meld!');
    },
    async handleStartNewRound() {
      await this.performAction(async () => {
        await roundsService.startRound(this.matchId);
        await this.loadCurrentRoundData();
      }, 'Failed to start new round!');
    },
    handleError(title, error) {
      this.$emit('error', title, error);
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
      await this.loadCurrentRoundData();
      this.initializeSSE();
    },
    async loadCurrentRoundData() {
      await this.loadCurrentTurn();
      await this.loadMyHand();
      await this.loadCurrentRoundDataForPlayers();
    },
    initializeSSE() {
      const latestActionId = this.latestActionId === null ? '' : this.latestActionId;
      const endpoint = `/matches/${this.matchId}/events?latest_action_id=${latestActionId}`;

      try {
        this.sseService = new SSEService(endpoint);

        this.sseService.connect(
            (data) => {
              const newCurrentRoundId = data.current_status.round_id;
              const newCurrentTurnId = data.current_status.turn_id;

              this.latestActionId = data.action.action_id;

              if (data.turn_id === this.currentTurnId) {
                this.currentTurnActions.push(data.action);
              }

              if (newCurrentRoundId !== this.currentRoundId) {
                this.currentRoundId = newCurrentRoundId;
                if (newCurrentRoundId === null) {
                  this.loadRoundDataForPlayers(data.round_id);
                } else {
                  this.loadCurrentRoundData();
                }
              } else if (newCurrentTurnId !== this.currentTurnId) {
                this.currentTurnId = newCurrentTurnId;
                this.loadCurrentTurn();
                this.loadCurrentRoundDataForPlayers();
              } else if (['draw', 'play_meld', 'extend_meld'].includes(data.action.action_type)) {
                // load changes to discard pile, stock pile, and melds — currently these all require reload of round data
                this.loadCurrentRoundDataForPlayers();
              }
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

  .game-section {
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
    flex-flow: row wrap;
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
