<template>
  <div id="app">
    <sign-in v-if="!isAuthenticated" @auth-success="handleAuthSuccess" />
    <div v-else class="authenticated">
      <create-match />
      <button @click="signOut">Sign Out</button>
    </div>
  </div>
</template>

<script>
import SignIn from './components/SignIn.vue';
import CreateMatch from './components/CreateMatch.vue';

export default {
  components: {
    SignIn,
    CreateMatch
  },
  data() {
    return {
      isAuthenticated: false,
    };
  },
  methods: {
    handleAuthSuccess() {
      this.isAuthenticated = true;
    },
    signOut() {
      localStorage.removeItem('token');
      this.isAuthenticated = false;
    }
  },
  created() {
    // Check if the token exists in localStorage when the app is created
    if (localStorage.getItem('token')) {
      this.isAuthenticated = true;
    }
  }
}
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

.authenticated {
  display: flex;
  flex-direction: column;
  align-items: center;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #f44336;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #e53935;
}
</style>
