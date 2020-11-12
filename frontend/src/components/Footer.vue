<template>
	<div class="footer-content">
		<a href="https://noiseorchestra.org/">Noise Orchestra</a> -
		<a href="https://github.com/noiseorchestra">GitHub</a> -
		<a href="https://twitter.com/orchestranoise?lang=en">Twitter</a>
	</div>
</template>

<script>
export default {
  name: 'Footer',
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

a {
	margin: 5px;
	color: map-get($colors, "dark");
	background-color: map-get($colors, "highlight");
}

#footer {
	// position: absolute;
	// z-index: 100;
	// left:0px;
	// top: 95vh;
	// height: 5vh;
	// min-width: 100vw;
	// margin: 4px;
}

.footer-content {
	// min-height: 12px;
	// max-width: 400px;
	text-align: center;
	padding: 8px;
}

</style>
