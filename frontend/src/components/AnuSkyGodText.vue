<template>
	<transition name="fade">
	  <div title="text" v-if="show">
			<p>Dedicated to the Ancient Ones, to the Sky Anu, Lord of Future who rides on a whispering south wind, to Addu, easier of storms who can fill the sky with brightness, to Indra and Thor for electricity burnt across the night sky, to Malah, Lord of Courage and Bravery, to Zahgurim whose number is twenty three, to Itzamna, Spirit of Early Mists and Showers, to Ixel Chel, the Spider-that-catches-the dew-of-Morning, to Kak U Pacat, who works in fire, to Schmuun, the Silent One, to the serpent Ouroboros, who encircles us all, to Pan, God of Panic, to the nameless gods of dispersal and emptiness, to Armillaria Ostoyae, endless formless network under our feet, to Hassan I Sabbah, Master of Rap Assasins.</p>

			<p>“Who grabbed a corner of the sky and thunder and lighting tore as they pulled it back and revealed what was underneath…”</p>

			<p>To all the scribes and artists and practitioners of magic through whom these spirits have been manifested…</p>

			<p>NOTHING IS TRUE. EVERYTHING IS PERMITTED</p>

			<p>After William S Burroughs’ Cities of the Red Night</p>
		</div>
	</transition>
</template>

<script>

export default {
  name: 'AnuSkyGodText',
	data () {
		return {
			show: false
		}
	},
	mounted() {
    this.show = true
  }
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";
@import url('https://fonts.googleapis.com/css?family=Fira+Mono:400');

div{
	padding: 10px;
	position: fixed;
  color: #fff;
	font-size: 30px;
  font-family: 'Fira Mono', monospace;
  letter-spacing: -7px;
	top: -2500px
}

.fade-enter-active, .fade-leave-active {
  transition: top 200s linear;
}
.fade-enter, .fade-leave-to {
  top: 0;
}

@media (min-width: map-get($breakpoints, "medium")) {
	div{
		font-size: 50px;
		padding: 10vh;
		top: -2000px
	}
}

</style>
