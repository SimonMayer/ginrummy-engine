<template>
  <div>
    <MatchTable
        ref="matchTable"
        :matchId="matchId"
        :players="players"
        :signedInUserId="signedInUserId"
        :loading="loading"
        @loading="updateLoading"
        @error="handleError"
    />
    <button v-if="canStartMatch" @click="startMatch">Start Match</button>
  </div>
</template>

<script>
import MatchTable from './MatchTable.vue';
import matchesService from '../services/matchesService';

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
    matchId: {
      type: Number,
      required: true
    },
    signedInUserId: {
      type: Number,
      required: true
    },
    loading: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    canStartMatch() {
      return this.players.length >= this.minPlayers && this.players.length <= this.maxPlayers && !this.match.start_time;
    }
  },
  data() {
    return {
      minPlayers: 2,
      maxPlayers: 4,
      players: []
    };
  },
  async created() {
    await this.loadPlayers();
  },
  methods: {
    updateLoading(loading) {
      this.$emit('update-loading', loading);
    },
    handleError(title, error) {
      this.$emit('error', title, error);
    },
    async loadPlayers() {
      this.updateLoading(true);
      try {
        this.players = await matchesService.getPlayers(this.matchId);
      } catch (error) {
        this.handleError('Failed to fetch players!', error);
      } finally {
        this.updateLoading(false);
      }
    },
    async startMatch() {
      if (!this.loading) {
        this.updateLoading(true);
        try {
          await matchesService.startMatch(this.matchId);
          await this.$refs.matchTable.loadAllData();
          this.$emit('match-started');
        } catch (error) {
          this.handleError('Failed to start match!', error);
        } finally {
          this.updateLoading(false);
        }
      }
    }
  }
};
</script>
