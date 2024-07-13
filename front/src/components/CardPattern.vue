<template>
  <div class="pattern">
    <div v-for="n in suitRepeat" :key="n" class="suit-symbol">{{ suitEmoji }}</div>
  </div>
</template>

<script>
export default {
  name: 'CardPattern',
  props: {
    suitEmoji: {
      type: String,
      required: true,
    },
    suitRepeat: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style scoped>
.pattern {
  position: absolute;
  top: var(--card-pattern-indentation-size);
  bottom: var(--card-pattern-indentation-size);
  left: var(--card-pattern-indentation-size);
  right: var(--card-pattern-indentation-size);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(16, 1fr);
  justify-content: center;
  justify-items: center;
  align-items: center;
}

.suit-symbol {
  font-size: var(--card-pattern-font-size);
}

/* Specific placement of each suit icon, for each rank */

/* rank 2 */
.card-content.rank-2 .suit-symbol:nth-child(1) {
  grid-column: 2;
  grid-row: 1 / span 4;
}

.card-content.rank-2 .suit-symbol:nth-child(2) {
  grid-column: 2;
  grid-row: 13 / span 4;
}

/* rank 3 */
.card-content.rank-3 .suit-symbol:nth-child(1) {
  grid-column: 2;
  grid-row: 1 / span 4;
}

.card-content.rank-3 .suit-symbol:nth-child(2) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

.card-content.rank-3 .suit-symbol:nth-child(3) {
  grid-column: 2;
  grid-row: 13 / span 4;
}

/* rank 4 */
.card-content.rank-4 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-4 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-4 .suit-symbol:nth-child(3) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-4 .suit-symbol:nth-child(4) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 5 */
.card-content.rank-5 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-5 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-5 .suit-symbol:nth-child(3) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

.card-content.rank-5 .suit-symbol:nth-child(4) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-5 .suit-symbol:nth-child(5) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 6 */
.card-content.rank-6 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-6 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-6 .suit-symbol:nth-child(3) {
  grid-column: 1;
  grid-row: 7 / span 4;
}

.card-content.rank-6 .suit-symbol:nth-child(4) {
  grid-column: 3;
  grid-row: 7 / span 4;
}

.card-content.rank-6 .suit-symbol:nth-child(5) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-6 .suit-symbol:nth-child(6) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 7 */
.card-content.rank-7 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(3) {
  grid-column: 2;
  grid-row: 4 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(4) {
  grid-column: 1;
  grid-row: 7 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(5) {
  grid-column: 3;
  grid-row: 7 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(6) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-7 .suit-symbol:nth-child(7) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 8 */
.card-content.rank-8 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(3) {
  grid-column: 2;
  grid-row: 4 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(4) {
  grid-column: 1;
  grid-row: 7 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(5) {
  grid-column: 3;
  grid-row: 7 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(6) {
  grid-column: 2;
  grid-row: 10 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(7) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-8 .suit-symbol:nth-child(8) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 9 */
.card-content.rank-9 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(3) {
  grid-column: 1;
  grid-row: 5 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(4) {
  grid-column: 3;
  grid-row: 5 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(5) {
  grid-column: 2;
  grid-row: 7 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(6) {
  grid-column: 1;
  grid-row: 9 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(7) {
  grid-column: 3;
  grid-row: 9 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(8) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-9 .suit-symbol:nth-child(9) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* rank 10 */
.card-content.rank-10 .suit-symbol:nth-child(1) {
  grid-column: 1;
  grid-row: 1 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(2) {
  grid-column: 3;
  grid-row: 1 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(3) {
  grid-column: 2;
  grid-row: 3 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(4) {
  grid-column: 1;
  grid-row: 5 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(5) {
  grid-column: 3;
  grid-row: 5 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(6) {
  grid-column: 1;
  grid-row: 9 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(7) {
  grid-column: 2;
  grid-row: 11 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(8) {
  grid-column: 3;
  grid-row: 9 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(9) {
  grid-column: 1;
  grid-row: 13 / span 4;
}

.card-content.rank-10 .suit-symbol:nth-child(10) {
  grid-column: 3;
  grid-row: 13 / span 4;
}

/* non-numeric cards */
.card-content.rank-A .suit-symbol:nth-child(1),
.card-content.rank-J .suit-symbol:nth-child(1),
.card-content.rank-Q .suit-symbol:nth-child(1),
.card-content.rank-K .suit-symbol:nth-child(1) {
  grid-column: 2;
  grid-row: 7 / span 4;
}
</style>
