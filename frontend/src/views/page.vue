<template>
  <div class="page-content">
    <PageContent :page="page" />
  </div>
</template>

<script>
import PageContent from '@/components/PageContent.vue';

export default {
  name: 'Page',
  components: {
    PageContent,
  },
  props: { page: Object },
};
</script>

<style scoped lang="scss">
@import '../scss/_variables.scss';

.page-content {
  /* width */
  &::-webkit-scrollbar {
    width: 12px;
  }

  /* Track */
  &::-webkit-scrollbar-track {
    background: map-get($colors, 'dark');
  }

  /* Handle */
  &::-webkit-scrollbar-thumb {
    background: map-get($colors, 'bright');
  }

  /* Handle on hover */
  &::-webkit-scrollbar-thumb:hover {
    background: map-get($colors, 'highlight');
  }

  color: map-get($colors, 'bright');
  overflow-y: auto;
  // max-height: 100%;
}
</style>
