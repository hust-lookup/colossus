<template>
  <q-item clickable v-ripple :to="{ path: props.nav}">
    <q-item-section avatar>
      <q-icon :name="props.icon"></q-icon>
    </q-item-section>

    <q-item-section> {{ props.sectionName }} </q-item-section>
  </q-item>
</template>
<script setup>

const props = defineProps({
  icon:{
    type: String,
    required: true
  },

  sectionName: {
    type: String,
    required: true
  },

  nav: {
    type: String,
    required: true,
    default:''
  }
});


</script>
<style lang=""></style>
