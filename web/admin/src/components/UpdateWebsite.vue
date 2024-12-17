<template>
  <q-dialog persistent>
    <q-card class="q-pa-lg">
      <span class="text-h6">{{ form_action_name }} Website</span>
      <q-form @submit="onSubmit">
        <q-card-section>
          <q-input
            filled
            v-model="form_web_name"
            label="Website name"
            stack-label
            hint="Website name"
          />
        </q-card-section>
        <q-card-section>
          <q-input
            filled
            v-model="form_web_url"
            label="Website url"
            stack-label
            hint="Website url"
          />
        </q-card-section>
        <q-card-section>
          <q-select
            filled
            v-model="form_status"
            label="Status"
            stack-label
            :options="statusOptions"
            behavior="menu"
          ></q-select>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup></q-btn>
          <q-btn flat type="submit" label="Confirm" color="primary" v-close-popup></q-btn>
        </q-card-actions>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref } from 'vue'
// import { collection, addDoc } from 'firebase/firestore'
// import { db } from '../firebase'

export default {
  props: {
    actionName: {
      type: String,
      default: '',
    },
    webName: {
      type: String,
      default: '',
    },
    webUrl: {
      type: String,
      default: '',
    },
    status: {
      type: String,
      default: 'Active',
    },

  },
   emits: ['update:modelValue'],
  setup(props) {
    const form_action_name = ref(props.actionName)
    const form_web_name = ref (props.webName)
    const form_web_url= ref(props.webUrl)
    const form_status= ref(props.status)

    return {
      statusOptions: ['Active', 'Disable'],
      form_action_name,
      form_web_name ,
      form_web_url,
      form_status ,
    }
  },
}
</script>

<style scoped>
.q-form {
  max-width: 400px;
  margin: auto;
}
</style>
