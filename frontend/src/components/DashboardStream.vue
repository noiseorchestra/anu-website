<template>
	<section class="live-stream">
		<b>Live Stream</b><br>
		<audio src="http://noiseaa2.miniserver.com:8000/curious_ear_stream" controls="true"/>
	</section>
</template>

<script>
export default {
  name: 'DashboardStream',
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.live-stream {color: map-get($colors, "bright");}
</style>
