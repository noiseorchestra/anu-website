<template>
  <main id="app">
    <Dashboard :naw="djangoData"></Dashboard>
  </main>
</template>

<script>
// @ is an alias to /src

import NavBar from '@/components/NavBar.vue'
import Dashboard from '@/components/Dashboard.vue'

export default {
  name: 'App',
  data: function() {
    return {
      djangoData: {
        name: 'Noise Orchestra Web',
        slug: 'noise-orchestra-web',
        about: 'About our web',
        owner: 'Noise Orchestra',
        jacktrip_hub_server: '123.123.123.123',
        influxdb: '234.234.243.234',
        stream_address: 'address_of_stream',
        file_storage: 'address_of_file_storage'
      }
    }
  },
  components: {
    Dashboard,
    NavBar
  },
  created: function () {
    if (document.getElementById('djangoData')) {
      console.log(JSON.parse(document.getElementById('djangoData').textContent))
      this.djangoData = JSON.parse(document.getElementById('djangoData').textContent)
    }
  },
}
</script>

<style lang="scss">
@import "@/scss/_common.scss";
@include base-style;
@include link-style;
</style>

<style scoped lang="scss">
@import "@/scss/_variables.scss";
</style>
