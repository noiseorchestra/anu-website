<template>
  <div class="page-body" tabindex="0">
    <div class="text-wrapper">
    <h1>{{page.title}}</h1>
      <div class="text" v-html="page.body"></div>
    </div>
    </div>
</template>

<script>
export default {
  name: 'PageContent',
  props: {page: Object},
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
      max-width: 100% !important;
      width: auto !important;
      max-height: 400px !important;
    }
  }
  overflow-x: hidden;
  background-color: map-get($colors, "dark");
  min-height: 100%;
}

.text-wrapper {
  padding: 20px;
}

</style>
