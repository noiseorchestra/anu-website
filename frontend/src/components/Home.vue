<template>
  <div class="home-container">
    <BackgroundLogo/>
  </div>
</template>

<script>
import BackgroundLogo from '@/components/BackgroundLogo.vue'

export default {
  name: 'Home',
  components: {
    BackgroundLogo
  }
}
</script>

<style scoped lang="scss">

.home-container {
  // max-height: 100vh;
  // min-height: 100vh;
  // width: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

</style>
