<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title> HUST App </q-toolbar-title>

      </q-toolbar>
    </q-header>
    <q-drawer v-model="leftDrawerOpen" show-if-above :width="270" :breakpoint="400">
      <q-scroll-area
        style="height: calc(100% - 150px); margin-top: 150px; border-right: 1px solid #ddd"
      >
        <q-list padding>
          <SideBar
          v-for="item in sideBarItems"
          :key="item.sectionName"
          v-bind="item"
          />
        </q-list>
      </q-scroll-area>

      <q-img
        class="absolute-top" 
        src="https://cdn.quasar.dev/img/material.png"
        style="height: 150px"
      >
        <div class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
          </q-avatar>
          <div class="text-weight-bold">{{user.first_name}} {{user.sur_name}}</div>
          <div>{{user.email}}</div>
        </div>
      </q-img>
    </q-drawer>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import SideBar from 'components/SideBar.vue'

const sideBarItems = [
  {
    icon: 'web',
    sectionName: 'Manage Websites',
    nav:('/home/manage_websites')
  },
  {
    icon: 'app_registration',
    sectionName: 'Manage Apps',
    nav:('/home/manage_apps')
  },
  {
    icon: 'view_stream',
    sectionName: 'Data',
    nav:('/home/datas')
  },
  {
    icon: 'model_training',
    sectionName: 'Models',
    nav:('/home/models')
  },
  {
    icon: 'assignment',
    sectionName: 'Logs',
    nav:('/home/logs')
  },
];

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

</script>
<script>
import axios from 'axios'

export default {
  data() {
    return {
      user: [],
      loading: false,
    }
  },
  methods: {
    fetchData() {
      this.loading = true
      const token = localStorage.getItem('token');
      console.log(token);
      
      axios
        .get('http://127.0.0.1:8000/users/me', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json',
          },
        })
        .then((response) => {
          this.user = response.data
          localStorage.setItem("user",this.user);
        })
        .catch((error) => {
          console.log(error)
        })
        .finally(() => {
          this.loading = false // Tắt loading sau khi nhận phản hồi
        })
    },
  },
  mounted() {
    this.fetchData()
  },
}
</script>
