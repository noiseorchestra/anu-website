<template>
  <article class="page-container">
    <div class="page-content">
      <div class="page-body" tabindex="0">
        <h1>{{pageBody.title}}</h1>
        <span class="text" v-html="pageBody.body"></span>
      </div>
    </div>
  </article>
</template>

<script>
export default {
  name: 'PageContent',
  props: {pageBody: Object},
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.page-container {
  max-height: calc(100vh - #{$header-height});
  max-width: 100vw;
}

.page-content {
  color: map-get($colors, "bright");
  padding-left: 10vw;
  padding-right: 10vw;
  overflow-y: auto;
  max-height: calc(100vh - #{$header-height});
  max-width: 100vw;
}

.page-body {
  overflow-y: auto;
  h1 {
    background-color: map-get($colors, "dark");
  }
  /deep/ p {
    background-color: map-get($colors, "dark");
  }
}

</style>
