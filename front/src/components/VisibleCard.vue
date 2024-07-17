<template>
  <div
      class="card visible-card"
      :class="{ selected: isSelected }"
      @click="handleClick"
      v-if="cardData"
  >
    <div :class="['card-content', rankClass, suitClass]">
      <CardCorner class="top-left" :rank="displayRank" :suit="suitEmoji"/>
      <CardPattern :suitEmoji="suitEmoji" :suitRepeat="suitRepeat"/>
      <CardCorner class="bottom-right" :rank="displayRank" :suit="suitEmoji"/>
    </div>
  </div>
</template>

<script>
import CardCorner from '@/components/CardCorner.vue';
import CardPattern from '@/components/CardPattern.vue';
import {getSuitEmoji, getDisplayRank, getSuitRepeat} from '@/utils/cardUtils';
import cardsService from '@/services/cardsService';

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
    },
    selectable: {
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
    handleClick() {
      if (this.selectable) {
        this.toggleSelection();
      }
    },
    emitUpdateSelected() {
      this.$emit('update:selected', this.cardData.card_id, this.isSelected);
    },
    toggleSelection() {
      this.isSelected = !this.isSelected;
      this.emitUpdateSelected();
    },
    unselect() {
      this.isSelected = false;
      this.emitUpdateSelected();
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

<style lang="scss" scoped>
@import '@/assets/globalVariables';
@import '@/assets/cards/variables.css';
@import '@/assets/cards/styles.css';

.card {
  user-select: none;
  transition: transform 0.3s ease, filter 0.3s ease;

  &.selected {
    filter: var(--card-selected-filter);
  }

  .card-content {
    position: relative;
    height: var(--card-height);
    border: 1px solid var(--card-edge-color);
    border-radius: var(--card-border-radius);
    background-color: var(--card-background-color);
    text-align: center;

    .top-left {
      top: var(--card-corner-indentation-size);
      left: 0;
    }

    .bottom-right {
      bottom: var(--card-corner-indentation-size);
      right: 0;
      transform: rotate(180deg);
    }

    &.spades {
      color: var(--card-suit-spades-color);
    }

    &.hearts {
      color: var(--card-suit-hearts-color);
    }

    &.clubs {
      color: var(--card-suit-clubs-color);
    }

    &.diamonds {
      color: var(--card-suit-diamonds-color);
    }
  }
}
</style>
