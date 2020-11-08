<template>
  <div class="vue-container vue-dashboard">
		<Dashboard :naw="naw"></Dashboard>
    <!-- <img src="../assets/anu-background-transparent.png"> -->
  </div>
</template>

<script>
import Dashboard from '@/components/Dashboard.vue'

export default {
  name: 'page',
  components: {
    Dashboard
  },
	props: {naw: Object},
}
</script>

<style scoped lang="scss">
@import "../scss/_variables.scss";
.vue-dashboard {
  position: absolute;
  padding-top: map-get($sizes, "header-height");
  min-height: calc(100vh - #{$header-height});
  min-width: 100vw;
}
</style>
