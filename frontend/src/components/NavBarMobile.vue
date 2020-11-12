<template>
	<span class="mobile-nav-wrapper">
	  <Slide v-bind:width="width" :closeOnNavigation="true">
			<router-link v-for="route in routes" :key="route.path" :to="route.path">
				{{route.name}}
			</router-link>
	  </Slide>
	</span>
</template>
<script>
import { Slide } from 'vue-burger-menu'  // import the CSS transitions you wish to use, in this case we are using `Slide`

export default {
	name: 'NavBar',
	props: {
		routes: Array
	},
	computed: {
		width() {
			console.log(window.innerWidth)
			if (window.innerWidth < 400) {
				return window.innerWidth;
			} else {
				return "400"
			}
		}
	},
  components: {
      Slide
  }
}
</script>

<style lang="scss">
@import "@/scss/_variables.scss";

.mobile-nav-wrapper {
	display: block;
}

@media (min-width: map-get($breakpoints, "medium")) {
	.mobile-nav-wrapper {
		display: none;
	}
}


.bm-burger-button {
	z-index: 300 !important;
	width: 20px !important;
	height: 20px !important;
	left: 5px !important;
	top: 5px !important;
}
.bm-burger-bars {
	background-color: map-get($colors, "highlight") !important;
}
.cross-style {
	top: 12px !important;
	right: 2px !important;
}
.bm-cross {
	background: map-get($colors, "bright") !important;
}
.bm-cross-button {
	height: 24px !important;
	width: 24px !important;
}
.bm-menu {
	height: 100%; /* 100% Full-height */
	width: 0; /* 0 width - change this with JavaScript */
	position: fixed; /* Stay in place */
	z-index: 1000; /* Stay on top */
	top: 0;
	left: 0;
	background-color: map-get($colors, "highlight") !important;
	overflow-x: hidden; /* Disable horizontal scroll */
	padding-top: 30px !important; /* Place content 60px from the top */
	transition: 0.5s; /*0.5 second transition effect to slide in the sidenav*/
}

.bm-overlay {
	background: map-get($colors, "bright") !important;
}
.bm-item-list {
	margin-left: 10% !important;
	font-size: 2em !important;
}
.bm-item-list > * {
	display: flex;
	text-decoration: none;
	padding: 0.7em;
}
.bm-item-list > * > span {
	margin-left: 10px;
	font-weight: 700;
	color: white;
}

</style>
