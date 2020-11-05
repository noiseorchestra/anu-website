<template>
  <div class="dashboard">
    <h2>{{naw.name}}</h2>
    <audio src="http://noiseaa2.miniserver.com:8000/curious_ear_stream" controls="true"/>
    <table>
      <tbody>
        <template v-for="(value, key) in naw">
            <tr>
            <td><b>{{key}}</b> : {{value}}</td>
            </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  props: {naw: Object},
}
</script>

<style lang="scss">
@import "@/scss/_variables.scss";
.dashboard {
  color: map-get($colors, "bright");
}

</style>
