<template>
  <div>
    <MatchTable
        :match="match"
        :players="players"
        :myHand="myHand"
        :signedInUserId="signedInUserId"
        :currentTurnUserId="currentTurnUserId"
        :loading="loading"
        @stock-pile-click="handleStockPileClick"
    />
    <button v-if="canStartMatch" @click="$emit('start-match')">Start Match</button>
  </div>
</template>

<script>
import MatchTable from './MatchTable.vue';

export default {
  name: 'MatchContent',
  components: {
    MatchTable,
  },
  props: {
    match: {
      type: Object,
      required: true
    },
    players: {
      type: Array,
      required: true
    },
    myHand: {
      type: Array,
      required: true
    },
    signedInUserId: {
      type: Number,
      required: true
    },
    currentTurnUserId: {
      type: [Number, null],
      required: true
    },
    loading: {
      type: Boolean,
      required: true
    },
    canStartMatch: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    handleStockPileClick() {
      this.$emit('stock-pile-click');
    }
  }
};
</script>

<style scoped>
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
