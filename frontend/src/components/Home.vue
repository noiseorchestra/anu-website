<template>
  <div class="home-container">
    <div @click="shouldShowLogo = false">
      <BackgroundLogo v-if="shouldShowLogo" />
      <div v-else>
        <div>
          <AnuSkyGod />
        </div>
      </div>
    </div>
    <div id="home-text"><h2>**** LISTEN TO THE LIVESTREAM <a href="/stream/">HERE</a>****</h2></div>
  </div>
</template>

<script>
import BackgroundLogo from '@/components/BackgroundLogo.vue';
import AnuSkyGod from '@/components/AnuSkyGod.vue';

export default {
  name: 'Home',
  components: {
    BackgroundLogo,
    AnuSkyGod,
  },
  data() {
    return { 
      shouldShowLogo: true };
  },
};
</script>

<style scoped lang="scss">
@import '@/scss/_variables.scss';

a {
  font-family: map-get($font, 'heading-family');
  padding: 4px;
}
.home-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

#home-text {
  color: map-get($colors, 'highlight');
  text-align: center;
  padding-bottom: 40px;
  h2 {
    font-size: 0.7em;
  }
}

@media (min-width: map-get($breakpoints, 'medium')) {
  #home-text {
    h2 {
      font-size: 1.5em;
    }
  }
}

</style>
