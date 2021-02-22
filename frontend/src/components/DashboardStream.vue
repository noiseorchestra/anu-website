<template>
  <section class="live-stream">
    <h2>Live Stream</h2>
    <audio
      src="https://icecast.autonomousnoiseunit.co.uk/stream"
      controls="true"
    />
  </section>
</template>

<script>
export default {
  name: 'DashboardStream',
};
</script>

<style scoped lang="scss">
@import '@/scss/_variables.scss';

.live-stream {
  color: map-get($colors, 'bright');
}
</style>
