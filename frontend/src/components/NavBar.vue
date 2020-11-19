<template>
	<nav id="desktop-nav" role="navigation">
		<ul>
			<li v-for="route in routes" v-if="route.title == 'Home'">
				<router-link :key="`/${route.slug}`" :to="`/${route.slug}`">
					{{route.title}}
				</router-link>
			</li>
			<li>
				<a class="nonav" href="#">
					About
				</a>
				<ul class="dropdown">
					<li v-for="route in routes" v-if="route.nav_parents == 'About'">
						<router-link :key="`/${route.slug}`" :to="`/${route.slug}`">
							{{route.title}}
						</router-link>
					</li>
				</ul>
			</li>
			<li>
				<a class="nonav" href="#">
					How To
				</a>
				<ul class="dropdown">
					<li v-for="route in routes" v-if="route.nav_parents == 'How To'">
						<router-link :key="`/${route.slug}`" :to="`/${route.slug}`">
							{{route.title}}
						</router-link>
					</li>
				</ul>
			</li>
		</ul>
	</nav>
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

ul {
list-style: none;
padding-left: 0;
padding-top: 0;
margin-block-start: 0px;
}

li {
display: block;
float: left;
position: relative;
text-decoration: none;
transition-duration: 0.5s;
}

li:hover {
cursor: pointer;
}

ul li ul {
width: 130px;
visibility: hidden;
opacity: 0;
min-width: 5rem;
position: absolute;
transition: all 0.5s ease;
display: none;
}

ul li:hover > ul,
ul li ul:hover {
  visibility: visible;
  opacity: 1;
  display: block;
}

ul li ul li {
clear: both;
  width: 100%;
}

#desktop-nav {
	padding-top: 4px;
	padding-left: 4px;
	display: none;
}

.nonav:hover {
	background-color: map-get($colors, "highlight");
}

@media (min-width: map-get($breakpoints, "medium")) {
	#desktop-nav {
		display: block;
	}
}


</style>
