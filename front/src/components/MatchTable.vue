<template>
  <div class="match-table">
    <StockPile
        v-if="match.stock_pile_size !== undefined"
        :size="match.stock_pile_size"
        @click="handleStockPileClick"
        :disabled="stockPileDisabled"
    />
    <MatchPlayerList
        :players="processedPlayers"
        :signedInUserId="signedInUserId"
        :currentTurnUserId="currentTurnUserId"
    />
  </div>
</template>

<script>
import StockPile from './StockPile.vue';
import MatchPlayerList from './MatchPlayerList.vue';

export default {
  name: 'MatchTable',
  components: {
    StockPile,
    MatchPlayerList,
  },
  props: {
    match: {
      type: Object,
      required: true,
    },
    players: {
      type: Array,
      required: true,
    },
    myHand: {
      type: Array,
      required: true,
    },
    signedInUserId: {
      type: Number,
      required: true,
    },
    currentTurnUserId: {
      type: [Number, null],
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
    stockPileDisabled: {
      type: Boolean,
      required: true,
    },
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
    }
  },
  methods: {
    handleStockPileClick() {
      this.$emit('stock-pile-click');
    },
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
