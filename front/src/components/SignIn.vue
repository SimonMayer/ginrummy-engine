<template>
  <div class="sign-in">
    <h1>Sign in</h1>
    <form @submit.prevent="signIn">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Sign in</button>
    </form>
  </div>
</template>

<script>
import apiClient from '../api/axios';

export default {
  name: 'SignIn',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async signIn() {
      try {
        const response = await apiClient.post('/auth/sign-in', {
          username: this.username,
          password: this.password
        });
        localStorage.setItem('rest_access_token', response.data.rest_access_token);
        localStorage.setItem('sse_access_token', response.data.sse_access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('user_id', response.data.user_id);

        this.$emit('auth-success');
      } catch (error) {
        alert('Sign in failed!');
        console.error(error);
      }
    }
  }
}
</script>

<style scoped>
.sign-in {
  display: flex;
  flex-direction: column;
  align-items: center;
}

form {
  display: flex;
  flex-direction: column;
  width: 300px;
}

input {
  margin-bottom: 10px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid var(--primary-color);
  border-radius: 5px;
  background-color: #f9f9f9;
}

button {
  padding: 10px;
  font-size: 16px;
}
</style>
