<template>
  <div id="app">
    <!-- <NavBar :routes=["home"]></NavBar> -->
    <Dashboard :naw="naw"></Dashboard>
  </div>
</template>

<script>
// @ is an alias to /src

import NavBar from '@/components/NavBar.vue'
import Dashboard from '@/components/Dashboard.vue'

export default {
  name: 'App',
  data: function() {
    return {naw: {}}
  },
  components: {
    Dashboard,
    NavBar
  },
  created: function () {
    let jsVariable = JSON.parse(document.getElementById('djangoData').textContent)
    this.naw = jsVariable.naw
    console.log(jsVariable.naw)
  },
}
</script>

<style>
#app {
  width: 95vw;
  color:white;
}

</style>
