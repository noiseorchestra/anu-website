<template>
  <div id="logo">
    <img id="background-logo" alt="ANU logo" :src="image" />
  </div>
</template>

<script>
export default {
  name: 'BackgroundLogo',
  data() {
    return {
      image: require('../../assets/ANU_FEST_BIG.png'),
    };
  },
};
</script>

<style scoped lang="scss">
@import '@/scss/_variables.scss';

#background-logo {
  max-height: 85vh;
  max-width: 100vw;
  padding-bottom: 0px;
}

@media (min-width: map-get($breakpoints, 'medium')) {
  #background-logo {
    padding-bottom: 0px;
  }
}
</style>
