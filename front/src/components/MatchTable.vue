<template>
  <div class="match-table">
    <StockPile
        v-if="match.stock_pile_size !== undefined"
        :size="match.stock_pile_size"
        @click="handleStockPileClick"
        :disabled="loading"
    />
    <MatchPlayerList
        :players="players"
        :myHand="myHand"
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
      type: Number,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
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
