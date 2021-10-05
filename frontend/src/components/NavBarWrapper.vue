<template>
  <span>
    <nav class="desktop-nav nav" aria-label="desktop-nav-bar">
      <NavBar :pages="mainNav"></NavBar>
    </nav>
    <nav class="mobile-nav nav" aria-label="mobile-nav-bar">
      <NavBarMobile :pages="mainNav"></NavBarMobile>
    </nav>
  </span>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import NavBarMobile from '@/components/NavBarMobile.vue';

export default {
  name: 'NavBarWrapper',
  components: {
    NavBar,
    NavBarMobile,
  },
  props: {
    pages: {
      type: Array,
      default: function () {
        return [];
      },
    },
  },
  computed: {
    mainNav: function () {
      return this.pages.filter((page) => {
        return page.nav_parents === 'none';
      });
    },
  },
};
</script>

<style scoped lang="scss">
@import '@/scss/_variables.scss';

.mobile-nav {
  display: inline;
  max-height: 0px;
  z-index: 1000;
}
</style>
