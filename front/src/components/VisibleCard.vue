<template>
  <div
      class="card visible-card"
      :class="{ selected: isSelected }"
      @click="toggleSelection"
      v-if="cardData"
  >
    <div :class="['card-content', rankClass, suitClass]">
      <CardCorner class="top-left" :rank="displayRank" :suit="suitEmoji" />
      <CardPattern :suitEmoji="suitEmoji" :suitRepeat="suitRepeat" />
      <CardCorner class="bottom-right" :rank="displayRank" :suit="suitEmoji" />
    </div>
  </div>
</template>

<script>
import CardCorner from './CardCorner.vue';
import CardPattern from './CardPattern.vue';
import { getSuitEmoji, getDisplayRank, getSuitRepeat } from '../utils/cardUtils';
import cardsService from "../services/cardsService";

export default {
  name: 'VisibleCard',
  components: {
    CardCorner,
    CardPattern,
  },
  props: {
    cardProp: {
      type: [Object, Number],
      required: true,
      validator(value) {
        if (typeof value === 'number') {
          return true;
        }
        return (
            value &&
            typeof value.card_id === 'number' &&
            typeof value.rank === 'string' &&
            typeof value.suit === 'string' &&
            typeof value.point_value === 'number'
        );
      }
    },
    selected: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      cardData: null,
      isSelected: this.selected
    };
  },
  computed: {
    suitEmoji() {
      return getSuitEmoji(this.cardData.suit);
    },
    displayRank() {
      return getDisplayRank(this.cardData.rank);
    },
    suitRepeat() {
      return getSuitRepeat(this.cardData.rank);
    },
    rankClass() {
      return `rank-${this.cardData.rank}`;
    },
    suitClass() {
      return this.cardData.suit.toLowerCase();
    },
  },
  methods: {
    toggleSelection() {
      this.isSelected = !this.isSelected;
      this.$emit('update:selected', this.cardData.card_id, this.isSelected);
    },
    isCardSelected() {
      return this.isSelected;
    }
  },
  async created() {
    if (typeof this.cardProp === 'number') {
      this.cardData = cardsService.getCard(this.cardProp);
    } else {
      this.cardData = this.cardProp;
    }
  }
};
</script>

<style scoped>
@import '../assets/cardStyles.css';

.card-content {
  position: relative;
  height: 150px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: white;
  text-align: center;
}

.top-left {
  top: 4px;
  left: 0px;
}

.bottom-right {
  bottom: 4px;
  right: 0px;
  transform: rotate(180deg);
}

.hearts, .diamonds {
  color: red;
}

.clubs, .spades {
  color: black;
}

.selected {
  transform: translateY(-20px);
  border: 2px solid #4CAF50;
}
</style>
