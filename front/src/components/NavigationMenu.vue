<template>
  <nav>
    <div class="nav-links">
      <router-link v-if="isAuthenticated" to="/create-match" custom v-slot="{ href, navigate, isActive, isExactActive }">
        <a :href="href" @click="navigate" :class="{ active: isActive, exactActive: isExactActive }">Create Match</a>
      </router-link>
      <router-link v-if="isAuthenticated" to="/matches" custom v-slot="{ href, navigate, isActive, isExactActive }">
        <a :href="href" @click="navigate" :class="{ active: isActive, exactActive: isExactActive }">Your Matches</a>
      </router-link>
    </div>
    <div class="auth-links">
      <router-link v-if="!isAuthenticated" to="/" custom v-slot="{ href, navigate, isActive, isExactActive }">
        <a :href="href" @click="navigate" :class="{ active: isActive, exactActive: isExactActive }">Sign In</a>
      </router-link>
      <a v-if="isAuthenticated" @click.prevent="signOut" href="#" class="sign-out">Sign Out</a>
    </div>
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

<style lang="scss" scoped>
@import '@/assets/globalVariables';

nav {
  display: flex;
  justify-content: space-between;
  gap: var(--base-margin);
  margin-bottom: var(--base-margin);
  background-color: var(--secondary-color);
  padding: var(--base-padding);
  border-radius: var(--border-radius);

  .nav-links, .auth-links {
    display: flex;
    gap: var(--base-margin);
  }

  a {
    color: var(--text-color);
    text-decoration: none;
    padding: var(--base-padding);
    border-radius: var(--border-radius);
    transition: background-color 0.3s, color 0.3s;

    &:hover {
      background-color: var(--button-hover-color);
    }

    &.active {
      font-weight: bold;
      border-bottom: solid 2px var(--accent-color);
    }
  }
}
</style>
