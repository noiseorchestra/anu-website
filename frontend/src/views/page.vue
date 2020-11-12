<template>
  <div class="page-content">
    <PageContent :pageBody="routeProps"></PageContent>
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

<style scoped lang="scss">
@import "../scss/_variables.scss";

.page-content {
  color: map-get($colors, "bright");
  // overflow-y: auto;
  // max-height: 100%;
}

@media (max-width: map-get($breakpoints, "small")) {
  .page-content {
    // padding-left: 5px;
    // padding-right: 5px;
  }
}

</style>
