<template>
	<div id="desktop-nav" aria-label="standard-nav-bar">
		<span class="nav-wrapper">
		<router-link v-for="route in routes" :key="route.path" :to="route.path">
			{{route.name}}
		</router-link>
	</span>
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

.nav-wrapper {
	display: none;
}

@media (min-width: map-get($breakpoints, "medium")) {
	.nav-wrapper {
		display: block;
	}
}


</style>
