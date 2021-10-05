<template>
  <a v-if="hasChildren" class="nav-link nonav" href="#">{{
    title
  }}</a>
  <router-link
    v-else
    :key="`/${slug}`"
    class="nav-link"
    :to="`/${slug}`"
  >
    {{ title }}
  </router-link>
</template>

<script>
export default {
  name: 'NavItem',
  props: {
    hasChildren: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: '',
    },
    slug: {
      type: String,
      default: '',
    },
  },
};
</script>

<style scoped lang="scss">
@import '@/scss/_variables.scss';
.nonav:hover {
  background-color: map-get($colors, 'highlight') !important;
  cursor: default !important;
}
</style>
