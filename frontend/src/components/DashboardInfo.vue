<template>
  <div class="dashboard-info">
    <div class="title"><h2>{{naw.name}}</h2></div>
    <div class="info">
      <div v-for="(value, key) in naw">
        <b>{{key}}</b> : {{value}}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardInfo',
  props: {naw: Object},
}
</script>

<style lang="scss">
@import "@/scss/_variables.scss";
.dashboard-info {
  color: map-get($colors, "bright");
  width: 100%;
  overflow-wrap: anywhere;
}

</style>
