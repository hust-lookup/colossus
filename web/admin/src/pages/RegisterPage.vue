<template>
  <div class="bg-light-blue-7 window-height window-width row justify-center items-center">
    <div class="column">
      <div class="row">
        <h5 class="text-h5 text-white q-my-md">HUST App</h5>
      </div>
      <div class="row">
        <q-card square bordered class="q-pa-lg shadow-1">
          <q-form class="q-gutter-md" @submit.prevent="registerUser">
            <q-card-section>
              <q-input
                square
                filled
                clearable
                v-model="email"
                type="email"
                label="Email"
                
                :rules="[val => !!val || 'Email is required']"
              />
              <q-input
                square
                filled
                clearable
                v-model="first_name"
                type="text"
                label="First Name"
                
                :rules="[val => !!val || 'First Name is required']"
              />
              <q-input
                square
                filled
                clearable
                v-model="sur_name"
                type="text"
                label="Sur Name"
                
                :rules="[val => !!val || 'Surname is required']"
              />
              <q-input
                square
                filled
                clearable
                v-model="password"
                type="password"
                label="Password"
                
                :rules="[val => val.length >= 6 || 'Password must be at least 6 characters']"
              />
              <q-input
                square
                filled
                clearable
                v-model="confirmed_password"
                type="password"
                label="Confirm Password"
                :rules="[ confirmPasswordRule ]"
              />
              <div v-if="passwordMismatch" class="text-negative">
                Passwords do not match!
              </div>
            </q-card-section>
            <q-card-actions class="q-px-md">
              <q-btn
                unelevated
                color="light-blue-7"
                size="lg"
                class="full-width"
                label="Register"
                type="submit"
                :disable="isSubmitDisabled"
              />
            </q-card-actions>
            <q-card-section class="text-center q-pa-none">
              <p class="text-grey-6">
                Already have an account?
                <router-link :to="'/login'">Back to Login</router-link>
              </p>
            </q-card-section>
          </q-form>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';

export default {
  setup() {
    // Các biến reactivity lưu trữ dữ liệu người dùng nhập vào
    const email = ref('');
    const first_name = ref('');
    const sur_name = ref('');
    const password = ref('');
    const confirmed_password = ref('');
    const router = useRouter();
    const $q = useQuasar();
    
    // Kiểm tra xem mật khẩu và mật khẩu xác nhận có khớp nhau không
    const passwordMismatch = computed(() => {
      return password.value !== confirmed_password.value && confirmed_password.value.length > 0;
    });

    // Rule để kiểm tra confirm password
    const confirmPasswordRule = passwordMismatch.value ? 'Passwords do not match' : true;

    // Kiểm tra trạng thái nút "Submit"
    const isSubmitDisabled = computed(() => {
      return !email.value || !first_name.value || !sur_name.value || password.value.length < 6 || passwordMismatch.value;
    });

    const registerUser = async () => {
      if (isSubmitDisabled.value) {
        // Nếu form không hợp lệ, ngăn gửi form
        $q.notify({
          color: 'negative',
          message: 'Please ensure all fields are filled correctly.',
          icon: 'error',
        });
        return;
      }

      const registerInfor = {
        email: email.value,
        first_name: first_name.value,
        sur_name: sur_name.value,
        password: password.value,
      };

      try {
        const response = await axios.post('http://127.0.0.1:8000/users/register', registerInfor, {
          headers: {
            accept: 'application/json',
            'Content-Type': 'application/json',
          },
        });

        if (response.status === 200) {
          console.log(response);
          router.push('/login') 
        } else {
          $q.notify({
            color: 'negative',
            message: 'Register failed, please check your credentials',
            icon: 'error',
          });
        }
      } catch (error) {
        console.log(error);

        $q.notify({
          color: 'negative',
          message: 'Register failed, please try again',
          icon: 'error',
        });
      }
    };

    return {
      email,
      first_name,
      sur_name,
      password,
      confirmed_password,
      passwordMismatch,
      confirmPasswordRule,
      isSubmitDisabled,
      registerUser,
    };
  },
};
</script>

<style>
.q-card {
  width: 450px;
}
</style>
