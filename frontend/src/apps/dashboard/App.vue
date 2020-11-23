<template>
  <DashboardView :naw="djangoData"></DashboardView>
</template>

<script>
// @ is an alias to /src

import DashboardView from '../../views/dashboard.vue'

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
    DashboardView,
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
@font-face {
  font-family: "Russian";
  src: url('../../../assets/fonts/Russian.woff') format('woff'), url('../../../assets/fonts/Russian.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: block;
}
@import "@/scss/_variables.scss";
@import "@/scss/_common.scss";
@include base-style;
@include link-style;
@include nav-style;
</style>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.container {
  width: 100%;
  padding: 30px;
}

</style>
