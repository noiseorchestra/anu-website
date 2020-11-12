<template>
	<div id="desktop-nav" aria-label="standard-nav-bar">
		<router-link v-for="route in routes" :key="route.path" :to="route.path">
			{{route.name}}
		</router-link>
	</div>
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

#desktop-nav {
	margin: 4px;
}

#desktop-nav a.router-link-exact-active {
	text-decoration: underline;
	font-weight: bold;
  color: map-get($colors, "dark");
}

#desktop-nav a {
	text-decoration: none;
	margin: 2px;
	font-weight: bold;
  color: map-get($colors, "dark");
}

</style>
