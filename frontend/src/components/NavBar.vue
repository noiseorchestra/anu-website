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
	display: flex;
	flex-direction: row;
}

@media (max-width: map-get($breakpoints, "small")) {
	.user{
		a {font-size: 20px;}
	}
	#desktop-nav {
		display: none;
	}
}


</style>
