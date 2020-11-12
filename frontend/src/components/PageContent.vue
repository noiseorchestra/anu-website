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
  .text {
    display: flex;
    flex-direction: column;
    /deep/img {
      border: 2px solid map-get($colors, "bright");
      align-self: center;
      height: auto !important;
      max-width: 400px !important;
      width: auto !important;
      max-height: 400px !important;
    }
  }
  overflow-y: auto;
  background-color: map-get($colors, "dark");
  text-align: justify;
  padding: 20px;

}

</style>
