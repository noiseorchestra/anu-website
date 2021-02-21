<template>
  <div class="dashboard-info">
    <div class="title">
      <h2>{{ naw.name }}</h2>
    </div>
    <div class="info">
      <div>
        <b>name</b> : {{ naw.name }}
      </div>
      <div>
        <b>owner</b> : {{ naw.owner }}
      </div>
      <div>
        <b>about</b> : {{ naw.about }}
      </div>
      <div>
        <b>stream url</b> : {{ naw.stream_address }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardInfo',
  props: {
    naw: {
      type: Object,
      default: function() {
        return {
          name: "Name",
          owner: "Owner",
          about: "about",
          stream_address: "Stream Address",
        }
      }
    }
  },
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
