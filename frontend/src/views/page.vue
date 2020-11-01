<template>
  <div class="vue-container vue-page">
		<PageContent :pageBody="routeProps.body"></PageContent>
    <!-- <img src="../assets/anu-background-transparent.png"> -->
  </div>
</template>

<script>
import PageContent from '@/components/PageContent.vue'

export default {
  name: 'page',
  components: {
    PageContent
  },
	props: {routeProps: Object},
}
</script>

<style scoped>
.vue-page {
  position: absolute;
  min-height: 100vh;
  min-width: 100vw;
}
</style>
