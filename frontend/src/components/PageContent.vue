<template>
  <div class="page-body" tabindex="0">
    <h1>{{pageBody.title}}</h1>
    <div class="text" v-html="pageBody.body"></div>
  </div>
</template>

<script>
export default {
  name: 'PageContent',
  props: {pageBody: Object},
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.page-body {
  overflow-y: auto;
  background-color: map-get($colors, "dark");
  text-align: justify;
  padding: 20px;
  // h1 {
  //   background-color: map-get($colors, "dark");
  // }
  // /deep/ p {
  //   background-color: map-get($colors, "dark");
  // }
}

</style>
