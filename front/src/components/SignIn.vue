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
import axios from 'axios';

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
        const response = await axios.post('http://localhost:5000/sign-in', {
          username: this.username,
          password: this.password
        });
        localStorage.setItem('token', response.data.token);
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
  margin-top: 50px;
}

h1 {
  margin-bottom: 20px;
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
}

button {
  padding: 10px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
