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
	font-size: 0.8rem;
}

.footer-content {
	width: 100%;
	text-align: center;
	// margin: 8px;
}

</style>
