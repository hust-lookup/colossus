<template>
  <div class="bg-light-blue-7 window-height window-width row justify-center items-center">
    <div class="column">
      <div class="row">
        <h5 class="text-h5 text-white q-my-md">HUST App</h5>
      </div>
      <div class="row">
        <q-card square bordered class="q-pa-lg shadow-1">
          <q-form class="q-gutter-md" @submit="loginUser">
            <q-card-section>
              <q-input
                square
                filled
                clearable
                v-model="email"
                type="email"
                label="email"
                class="q-mb-md"
              />
              <q-input
                square
                filled
                clearable
                v-model="password"
                type="password"
                label="password"
              />
            </q-card-section>
            <q-card-actions class="q-px-md">
              <q-btn
                unelevated
                color="light-blue-7"
                size="lg"
                class="full-width"
                label="Login"
                type="submit"
              />
            </q-card-actions>
          </q-form>
          <q-card-section class="text-center q-pa-none">
            <p class="text-grey-6">Not reigistered? <router-link :to="'/register'">Created an Account</router-link></p>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    async loginUser() {
      try {
        const loginInfor = JSON.stringify({
          email: this.email,
          password: this.password,
        })
        const response = await axios.post('http://127.0.0.1:8000/users/login', loginInfor, {
          headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json',
          },
        })
        if (response.status === 200) {
          console.log(response);
          
          localStorage.setItem('token', response.data.access_token) 
          this.$router.push('/home') 
        } else {
          this.$q.notify({
            color: 'negative',
            message: 'Login failed, please check your credentials',
            icon: 'error',
          })
        }
      } catch (error) {
        console.log(error)

        this.$q.notify({
          color: 'negative',
          message: 'Login failed, please try again',
          icon: 'error',
        })
      }
    },
  },
}
</script>

<style>
.q-card {
  width: 400px;
}
</style>
