<template>
  <nav>
    <router-link v-if="!isAuthenticated" to="/" custom v-slot="{ href, navigate, isActive, isExactActive }">
      <a :href="href" @click="navigate" :class="{ active: isActive, exactActive: isExactActive }">Sign In</a>
    </router-link>
    <router-link v-if="isAuthenticated" to="/create-match" custom v-slot="{ href, navigate, isActive, isExactActive }">
      <a :href="href" @click="navigate" :class="{ active: isActive, exactActive: isExactActive }">Create Match</a>
    </router-link>
    <router-link v-if="isAuthenticated" to="/matches" custom v-slot="{ href, navigate, isActive, isExactActive }">
      <a :href="href" @click="navigate" :class="{ active: isActive, exactActive: isExactActive }">Your Matches</a>
    </router-link>
    <button v-if="isAuthenticated" @click="signOut">Sign Out</button>
  </nav>
</template>

<script>
export default {
  name: 'NavigationMenu',
  props: {
    isAuthenticated: {
      type: Boolean,
      required: true
    },
    signOut: {
      type: Function,
      required: true
    }
  }
};
</script>

<style scoped>
nav {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
}

a {
  color: #333;
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 3px;
  transition: background-color 0.3s;
}

a:hover {
  background-color: #ddd;
}

a.active {
  font-weight: bold;
  background-color: #4CAF50; /* Highlight color for active link */
  color: white;
}

button {
  padding: 5px 10px;
  font-size: 16px;
  background-color: #f44336;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 3px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #e53935;
}
</style>
