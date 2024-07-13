<template>
  <div class="match-details">
    <ErrorBox v-if="errorTitle" :title="errorTitle" :message="errorMessage" @close="clearErrorBox" />
    <h1>Match ID: {{ matchId }}</h1>
    <LoadingIndicator :visible="loading" />
    <MatchContent
        :match="match"
        :matchId="matchId"
        :signedInUserId="signedInUserId"
        :loading="loading"
        @update-loading="updateLoading"
        @error="handleError"
        @match-started="loadMatchDetails"
    />
  </div>
</template>

<script>
import matchesService from '../services/matchesService';
import { setErrorMessage, clearErrorMessage } from '../utils/errorHandler';
import ErrorBox from './ErrorBox.vue';
import LoadingIndicator from './LoadingIndicator.vue';
import MatchContent from './MatchContent.vue';

export default {
  name: 'MatchDashboard',
  components: {
    ErrorBox,
    LoadingIndicator,
    MatchContent,
  },
  data() {
    return {
      matchId: parseInt(this.$route.params.id, 10),
      match: {
        create_time: '',
        created_by: null,
        end_time: null,
        match_id: null,
        start_time: null,
      },
      loading: true,
      errorTitle: '',
      errorMessage: '',
      signedInUserId: parseInt(localStorage.getItem('user_id'), 10),
    };
  },
  async created() {
    await this.loadData([
      { method: this.loadMatchDetails, errorTitle: 'Failed to fetch match details!' }
    ]);
  },
  methods: {
    async loadData(tasks) {
      for (const {method, errorTitle} of tasks) {
        await this.handleApiCall(method, errorTitle);
      }
    },
    async handleApiCall(apiCall, errorTitle) {
      this.loading = true;
      try {
        await apiCall();
      } catch (error) {
        setErrorMessage(this, errorTitle, error);
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    async loadMatchDetails() {
      this.match = await matchesService.getMatchDetails(this.matchId);
      this.match.match_id = this.matchId; // Ensure match_id is set
    },
    updateLoading(loading) {
      this.loading = loading;
    },
    handleError(title, error) {
      setErrorMessage(this, title, error);
    },
    clearErrorBox() {
      clearErrorMessage(this);
    },
  },
};
</script>

<style scoped>
.match-details {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
