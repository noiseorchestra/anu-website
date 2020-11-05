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

a {
	margin-right: 5px;
}

#nav {
	position: absolute;
	z-index: 100;
	left:0px;
	top: 0px;
	padding: 4px;
}

#nav a.router-link-exact-active {
	font-weight: bold;
  color: map-get($colors, "dark");
}

#nav a {
  color: map-get($colors, "dark");
}

</style>
