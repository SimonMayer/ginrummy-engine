<template>
  <div class="match-list">
    <h1>Your Matches</h1>
    <ul>
      <li v-for="match in sortedMatches" :key="match.match_id">
        <router-link :to="`/matches/${match.match_id}`">
          <p>Match ID: {{ match.match_id }}</p>
          <p>Create Time: {{ formatDateTime(match.create_time) }}</p>
          <p v-if="match.start_time">Start Time: {{ formatDateTime(match.start_time) }}</p>
          <p v-if="match.end_time">End Time: {{ formatDateTime(match.end_time) }}</p>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import apiClient from '@/api/axios';
import { formatDateTime } from '@/utils/dateFormatter';

export default {
  name: 'MatchList',
  data() {
    return {
      matches: [],
    };
  },
  async created() {
    try {
      const response = await apiClient.get('/matches');
      this.matches = response.data;
    } catch (error) {
      alert('Failed to fetch matches!');
      console.error(error);
    }
  },
  computed: {
    sortedMatches() {
      return this.matches.slice().sort((a, b) => new Date(b.create_time) - new Date(a.create_time));
    }
  },
  methods: {
    formatDateTime
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/globalVariables';

.match-list {
  display: flex;
  flex-direction: column;
  align-items: center;

  ul {
    list-style-type: none;
    padding: 0;
    width: 100%;

    li {
      background-color: var(--secondary-color);
      padding: 15px;
      margin: 10px 0;
      border-radius: 5px;
      transition: background-color 0.3s, box-shadow 0.3s;

      &:hover {
        background-color: var(--button-hover-color);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      }

      p {
        margin: 5px 0;
        color: var(--text-color);
      }

      a {
        text-decoration: none;
        color: inherit;
      }
    }
  }
}
</style>
