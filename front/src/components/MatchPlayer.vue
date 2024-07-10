<template>
  <li :class="['player-item', { 'highlighted': highlightPlayer }]">
    {{ username }}
    <ul class="hand" v-if="hiddenCardCount">
      <li v-for="n in hiddenCardCount" :key="n" class="card-item">
        <HiddenCard />
      </li>
    </ul>
    <ul class="hand" v-if="hand">
      <li
          v-for="card in hand"
          :key="card.card_id"
          :class="['card-item', { selected: isSelectedCard(card), selectable: selectable }]"
          @click="handleCardClick(card)"
      >
        <VisibleCard :cardProp="card" />
      </li>
    </ul>
  </li>
</template>

<script>
import HiddenCard from './HiddenCard.vue';
import VisibleCard from './VisibleCard.vue';

export default {
  name: 'MatchPlayer',
  components: {
    HiddenCard,
    VisibleCard
  },
  props: {
    username: {
      type: String,
      required: true
    },
    hand: {
      type: Array,
      required: true
    },
    hiddenCardCount: {
      type: Number,
      required: true,
      default: 0
    },
    highlightPlayer: {
      type: Boolean,
      default: false
    },
    selectable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      selectedCards: []
    };
  },
  computed: {
    isSelectedCard() {
      return (card) => this.selectedCards.some(selected => selected.card_id === card.card_id);
    }
  },
  methods: {
    handleCardClick(card) {
      if (this.selectable) {
        const index = this.selectedCards.findIndex(selected => selected.card_id === card.card_id);
        if (index === -1) {
          this.selectedCards.push(card);
        } else {
          this.selectedCards.splice(index, 1);
        }
        this.$emit('update:selectedCards', this.selectedCards);
      }
    }
  }
};
</script>

<style scoped>
.player-item {
  background-color: #f9f9f9;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ddd;
}

.highlighted {
  border: 2px solid #4CAF50;
  background-color: #e8f5e9;
}

.hand {
  display: flex;
  flex-direction: row;
  padding: 0;
  margin: 10px 0 0 0;
  list-style-type: none;
}

.card-item {
  transition: transform 0.3s ease;
}

.card-item.selectable {
  cursor: pointer;
}

.card-item.selected {
  transform: translateY(-20px);
}

.card-item:not(:first-child) {
  margin-left: -80px;
}
</style>
