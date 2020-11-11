<template>
	<div id="logo">
	  <img id="background-logo" alt="ANU logo" v-bind:src="image"></img>
	</div>
</template>

<script>

export default {
  name: 'BackgroundLogo',
	data () {
    return {
      image: require('../../assets/WEB_LOGO_TEXT.png'),
    }
  },
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

#background-logo {
		max-height: 500px;
}
@media (max-width: map-get($breakpoints, "small")) {
	#background-logo {
		max-height: 200px;
	}
}

</style>
