<template>
	<nav id="nav">
    <Slide width="360">
			<router-link v-for="route in routes" :key="route.path" :to="route.path">
				{{route.name}}
			</router-link>
    </Slide>
	</nav>
</template>
<script>
import { Slide } from 'vue-burger-menu'  // import the CSS transitions you wish to use, in this case we are using `Slide`

export default {
	name: 'NavBar',
	props: {
		routes: Array
	},
  components: {
      Slide
  }
}
</script>

<style lang="scss">
@import "@/scss/_variables.scss";

// .slide {
// 	width: 100vm;
// }

// @media (max-width: map-get($breakpoints, "medium")) {
// 	.slide {
// 		width: 300px;
// 	}
// }

.bm-burger-button {
	z-index: 300;
	position: fixed;
	width: 36px;
	height: 30px;
	left: 36px;
	top: 36px;
	cursor: pointer;
}
.bm-burger-bars {
	background-color: map-get($colors, "highlight");
}
.line-style {
	position: absolute;
	height: 20%;
	left: 0;
	right: 0;
}
.cross-style {
	position: absolute;
	top: 12px;
	right: 2px;
	cursor: pointer;
}
.bm-cross {
	background: map-get($colors, "bright");
}
.bm-cross-button {
	height: 24px;
	width: 24px;
}
.bm-menu {
	height: 100%; /* 100% Full-height */
	width: 0; /* 0 width - change this with JavaScript */
	position: fixed; /* Stay in place */
	z-index: 1000; /* Stay on top */
	top: 0;
	left: 0;
	background-color: map-get($colors, "dark");
	overflow-x: hidden; /* Disable horizontal scroll */
	padding-top: 60px; /* Place content 60px from the top */
	transition: 0.5s; /*0.5 second transition effect to slide in the sidenav*/
}

.bm-overlay {
	background: map-get($colors, "dark");
}
.bm-item-list {
	a {
		color: map-get($colors, "bright");
		background-color: map-get($colors, "dark");}
	a.router-link-exact-active {
		font-weight: bold;
		color: map-get($colors, "bright");
	}
	margin-left: 10%;
	font-size: 20px;
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
