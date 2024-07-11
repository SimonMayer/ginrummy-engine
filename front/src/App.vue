<template>
  <div id="app">
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

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}
</style>
