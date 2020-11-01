<template>
  <div class="page-container">
    <div class="page-content"><div class="page-body" v-html='pageBody'></div></div>
  </div>
</template>

<script>
export default {
  name: 'PageContent',
  props: {pageBody: String},
}
</script>

<style scoped>

.page-container {
  max-height: 100vh;
}

.page-content {
  color: white;
  padding-left: 10vw;
  padding-right: 10vw;
  padding-top: 10vh;
  margin-top: 5vh;
  padding-bottom: 15vh;
  overflow-y: auto;
  max-height: 70vh;
}

.page-body {
  padding-bottom: 100vh;
}

</style>
