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
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

</style>
