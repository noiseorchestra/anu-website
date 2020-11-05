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
  max-height: 100vh;
}

.page-content {
  color: map-get($colors, "bright");
  padding-left: 10vw;
  padding-right: 10vw;
  padding-top: 10vh;
  margin-top: 5vh;
  padding-bottom: 15vh;
  overflow-y: auto;
  max-height: 70vh;
}

.page-body {
  overflow-y: auto;
  padding-bottom: 100vh;
  /deep/ p {
    background-color: map-get($colors, "dark");
  }
}

</style>
