<template>
  <div id="app">
    <nav>
      <router-link to="/">Sign In</router-link>
      <router-link v-if="isAuthenticated" to="/create-match">Create Match</router-link>
      <router-link v-if="isAuthenticated" to="/matches">Your Matches</router-link>
      <button v-if="isAuthenticated" @click="signOut">Sign Out</button>
    </nav>
    <router-view @auth-success="handleAuthSuccess" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const isAuthenticated = ref(false);
    const router = useRouter();

    const handleAuthSuccess = () => {
      isAuthenticated.value = true;
      router.push('/matches');
    };

    const signOut = () => {
      localStorage.removeItem('token');
      isAuthenticated.value = false;
      router.push('/');
    };

    onMounted(() => {
      if (localStorage.getItem('token')) {
        isAuthenticated.value = true;
      }
    });

    return {
      isAuthenticated,
      handleAuthSuccess,
      signOut
    };
  }
};
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

nav {
  margin-bottom: 20px;
}

button {
  margin-left: 10px;
  padding: 5px 10px;
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
