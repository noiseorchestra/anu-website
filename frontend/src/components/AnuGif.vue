<template>
  <div
    class="anu-img"
    :class="{blink: blink}"
    :style="{top:top + 'px', left:left + 'px'}"
  >
    <img
      alt="ANU gif"
      :src="src"
    >
  </div>
</template>

<script>

export default {
  name: 'AnuGif',
	data () {
    return {
			blink: false,
      image: require('../../assets/anu-line-small.png'),
      gif: require('../../assets/anu.gif'),
    }
  },
	computed: {
		src() {
			if(2 * Math.random() < 1) {
				this.blink = true
				return this.image
			} else {
				return this.gif
			}
		},
		top() {
			return Math.random() * (window.innerHeight);
		},
		left(){
			return Math.random() * (window.innerWidth);
		}
	},
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.anu-img {
	z-index: 100;
	position: fixed;
	width: 10vh;
	min-width: 80px;
}

img {
	display: block;
	max-width: 10vw;
	height: auto;
	min-width: 80px;
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
