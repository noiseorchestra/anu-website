<template>
	<div class="nav-wrapper">
		<div id="desktop-nav" aria-label="standard-nav-bar">
			<div class="nav-dropdown">
				<div class="nav-item header" v-for="route in routes">
					<router-link v-if="route.title == 'Home'" :key="`/${route.slug}`" :to="`/${route.slug}`">
						{{route.title}}
					</router-link>
				</div>
			</div>
			<div class="nav-dropdown">
				<div class="nav-item header"><a>About</a></div>
				<div class="nav-items">
					<div class="nav-item" v-for="route in routes">
						<router-link v-if="route.nav_parents == 'About'" :key="`/${route.slug}`" :to="`/${route.slug}`">
							{{route.title}}
						</router-link>
					</div>
				</div>
			</div>
			<div class="nav-dropdown">
				<div class="nav-item header"><a>How To</a></div>
				<div class="nav-items">
					<div class="nav-item" v-for="route in routes">
						<router-link v-if="route.nav_parents == 'How To'" :key="`/${route.slug}`" :to="`/${route.slug}`">
							{{route.title}}
						</router-link>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
    routes: Array
  },
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

#desktop-nav {
	padding-top: 4px;
	padding-left: 4px;
	display: flex;
	flex-direction: row;
}

.nav-wrapper {
	display: none;
}

.nav-dropdown {
	display: flex;
	flex-direction: column;
	max-height: 18px;
	overflow: hidden;
}

.nav-item {
	&.header {
		cursor: pointer;
	}
}

.nav-dropdown:hover {
	max-height: 300px;
}

@media (min-width: map-get($breakpoints, "medium")) {
	.nav-wrapper {
		display: block;
	}
}


</style>
