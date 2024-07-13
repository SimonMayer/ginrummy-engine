<template>
  <div class="container">
    <NavigationMenu :isAuthenticated="isAuthenticated" :signOut="signOut" />
    <router-view @auth-success="handleAuthSuccess" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import NavigationMenu from '@/components/NavigationMenu.vue';

export default {
  name: 'App',
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

<style lang="scss">
@import '@/assets/globalVariables';
@import '@/assets/globalStyles';
</style>

<style lang="scss" scoped>
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

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--base-padding);
  box-sizing: border-box;
}
</style>
