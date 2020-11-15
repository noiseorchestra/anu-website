<template>
	<div class="gif-container">
	  <div class="gif-item" ><img alt="ANU gif" v-bind:src="gif"></img></div>
	  <div class="gif-item blink" ><img alt="ANU gif" v-bind:src="image"></img></div>
	  <div class="gif-item" ><img alt="ANU gif" v-bind:src="gif"></img></div>
	  <div class="gif-item blink" ><img alt="ANU gif" v-bind:src="image"></img></div>
	  <div class="gif-item" ><img alt="ANU gif" v-bind:src="gif"></img></div>
	</div>
</template>

<script>

export default {
  name: 'AnuGif',
	data () {
    return {
      image: require('../../assets/anu-line.png'),
      gif: require('../../assets/anu.gif'),
    }
  },
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.gif-container {
	height: 100%;
	display: flex;
	flex-direction: column;
	justify-content: space-around;
	align-items: center;
}

.gif-item {
	flex: 1;
}

img {
	display: block;
	max-width: 100px;
	height: auto;
}

.blink {
  animation: blinker 1s linear infinite;
}

@keyframes blinker {
  50% {
    opacity: 0;
  }
}

</style>
