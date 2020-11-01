<template>
	<footer id="footer">
		<div class="footer-content">
			<a href="https://noiseorchestra.org/">Noise Orchestra</a> -
			<a href="https://github.com/noiseorchestra">GitHub</a> -
			<a href="https://twitter.com/orchestranoise?lang=en">Twitter</a>
		</div>
	</footer>
</template>

<script>
export default {
  name: 'Footer',
}
</script>

<style scoped>

a {
	margin: 5px;
	color: black;
	background-color: #fdd01c;
}

#footer {
	position: absolute;
	z-index: 100;
	left:0px;
	top: 95vh;
	height: 5vh;
	min-width: 100vw;
	padding: 0;
}

.footer-content {
	min-height: 12px;
	max-width: 400px;
	text-align: center;
	margin: 0 auto;
}

</style>
