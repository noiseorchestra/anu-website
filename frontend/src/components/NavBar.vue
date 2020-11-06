<template>
	<nav id="nav">
		<router-link v-for="route in routes" :key="route.path" :to="route.path">
			{{route.name}}
		</router-link>
	</nav>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
    routes: Array
  }
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

#nav {
	display: block;
	position: fixed;
	margin: 4px;
	z-index: 100;
	left:0px;
	top: 0px;
	height: map-get($sizes, "header-height");
	width: 100vw;
}

#nav a.router-link-exact-active {
	text-decoration: underline;
	margin: 2px;
	font-weight: bold;
  color: map-get($colors, "dark");
}

#nav a {
	text-decoration: none;
	margin: 2px;
	font-weight: bold;
  color: map-get($colors, "dark");
}

</style>
