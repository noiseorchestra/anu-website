<template>
	<div id="logo">
	  <img id="background-logo" v-bind:src="image"></img>
	  <img id="background-text" v-bind:src="text"></img>
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

<style>
#logo {
		width: 300px;
		padding-bottom: 50px;
}
/* #background-logo {
		width: 300px;
		padding-bottom: 50px;
} */
</style>
