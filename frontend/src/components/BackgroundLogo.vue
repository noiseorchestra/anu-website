<template>
  <div id="logo">
    <img
      id="background-logo"
      alt="ANU logo"
      :src="image"
    >
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
	max-height: 85vh;
	padding-bottom: 40px;
}

@media (min-width: map-get($breakpoints, "medium")) {
	#background-logo {
		padding-bottom: 20px;
	}
}

</style>
