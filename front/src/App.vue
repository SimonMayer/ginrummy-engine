<template>
  <div class="container">
    <NavigationMenu :isAuthenticated="isAuthenticated" :signOut="signOut" />
    <router-view @auth-success="handleAuthSuccess" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import NavigationMenu from './components/NavigationMenu.vue';

export default {
  components: {
    NavigationMenu
  },
  setup() {
    const isAuthenticated = ref(false);
    const router = useRouter();

    const handleAuthSuccess = () => {
      isAuthenticated.value = true;
      router.push('/matches');
    };

    const signOut = () => {
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('rest_access_token');
      localStorage.removeItem('sse_access_token');
      isAuthenticated.value = false;
      router.push('/');
    };

    onMounted(() => {
      if (localStorage.getItem('refresh_token')) {
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

<style>
:root {
  --primary-color: #1B5E20;
  --secondary-color: #233D4D;
  --secondary-color-rgb: 35, 61, 77;
  --tertiary-color: #7CA982;
  --accent-color: #F7B32B;
  --button-hover-color: #7CA982;
  --button-active-color: #FE7F2D;
  --disabled-color: #B0BEC5;
  --text-color: #ffffff;
  --error-color: #9b1d20;
  --error-accent-color: #DA2C38;
  --font-family: 'Roboto', sans-serif;
  --base-padding: 10px;
  --base-margin: 10px;
  --border-radius: 5px;
}

body {
  font-family: var(--font-family);
  color: var(--text-color);
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  background-size: cover;
  background-attachment: fixed;
  margin: 0;
  padding: var(--base-padding);
}

#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--text-color);
  background-image: url('data:image/svg+xml,%3Csvg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="%231b5e20" fill-opacity="0.5"%3E%3Cpath d="M0 0h50v50H0zM50 50h50v50H50zM0 50h50v50H0zM50 0h50v50H50z"/%3E%3C/g%3E%3C/svg%3E%3E');
  background-size: 200px 200px;
  background-blend-mode: overlay;
  min-height: 100vh;
}

button {
  background-color: var(--secondary-color);
  color: var(--text-color);
  border: solid 1px var(--tertiary-color);
  border-radius: var(--border-radius);
  padding: var(--base-padding) calc(2 * var(--base-padding));
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

button:disabled {
  background-color: var(--disabled-color);
}

button:not(:disabled):hover {
  background-color: var(--button-hover-color);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

button:not(:disabled):active {
  background-color: var(--button-active-color);
}

button:focus {
  outline: none;
}

h1, h2, h3, h4, h5, h6 {
  margin: 0;
  padding: 0;
  color: var(--accent-color);
}

h1 {
  margin-bottom: 20px;
}

p {
  margin: 0 0 1em;
}

a {
  color: var(--accent-color);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}
</style>
