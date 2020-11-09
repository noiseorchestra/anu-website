<template>
	<div id="logo">
	  <img id="background-logo" alt="ANU logo" v-bind:src="image"></img>
	  <img id="background-text" alt="ANU text logo" v-bind:src="text"></img>
	</div>
</template>

<script>

export default {
  name: 'BackgroundLogo',
	data () {
    return {
      image: require('../../assets/ANU_YELLOW_LOGO.png'),
      text: require('../../assets/TEXT_YELLOW.png'),
    }
  },
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";
#logo {
		width: 200px;
		padding-bottom: 50px;
}
#background-text {
		width: 200px;
}
#background-logo {
		width: 200px;
}
@media (max-width: map-get($breakpoints, "small")) {
	#logo {
			width: 100px;
			padding-bottom: 20px;
	}
	#background-text {
			width: 100px;
	}
	#background-logo {
			width: 100px;
	}
}

</style>
