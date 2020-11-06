<template>
  <div class="vue-container vue-page">
		<PageContent :pageBody="routeProps"></PageContent>
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
  padding-top: 50px;
  min-height: calc(100vh - 50px);;
  min-width: 100vw;
}
</style>
