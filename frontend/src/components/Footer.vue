<template>
  <div class="footer-content">
    <a class="nav-link" href="https://noiseorchestra.org/">Noise Orchestra</a> -
    <a class="nav-link" href="https://github.com/noiseorchestra">GitHub</a> -
    <a class="nav-link" href="/contact">Contact</a>
  </div>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

a {
  font-size: 0.8rem;
}

.footer-content {
  width: 100%;
  text-align: center;
  // margin: 8px;
}
</style>
