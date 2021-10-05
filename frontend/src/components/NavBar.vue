<template>
  <nav
    id="desktop-nav"
    aria-label="standard-nav-bar"
    role="navigation"
  >
    <ul>
      <li v-for="page in pages" :key="page.slug">
        <NavItem
          :hasChildren="page.nav_children.length > 0"
          v-bind="page"
        />
        <ul v-if="page.nav_children.length > 0" class="dropdown">
          <li
            v-for="navChild in page.nav_children"
            :key="navChild.slug"
          >
            <NavItem :hasChildren="false" v-bind="navChild" />
          </li>
        </ul>
      </li>
    </ul>
  </nav>
</template>

<script>
import NavItem from '@/components/NavItem.vue';

export default {
  name: 'NavBar',
  components: {
    NavItem,
  },
  props: {
    pages: {
      type: Array,
      default: function () {
        return [];
      },
    },
  },
};
</script>

<style scoped lang="scss">
@import '@/scss/_variables.scss';

#desktop-nav {
  padding-top: 4px;
  padding-left: 4px;
  display: none;
}

@media (min-width: map-get($breakpoints, 'medium')) {
  #desktop-nav {
    display: block;
  }
}

ul {
  list-style: none;
  padding-left: 0;
  margin-block-start: 0px;
}

li {
  display: block;
  float: left;
  padding-top: 2px;
  position: relative;
  text-decoration: none;
  transition-duration: 0.5s;
}

li:hover {
  cursor: pointer;
}

ul li ul {
  width: 200px;
  visibility: hidden;
  opacity: 0;
  min-width: 5rem;
  position: absolute;
  transition: all 0.5s ease;
  display: none;
}

ul li:hover > ul,
ul li ul:hover {
  visibility: visible;
  opacity: 1;
  display: block;
}

ul li ul li {
  clear: both;
  width: 100%;
}
</style>
