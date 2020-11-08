<template>
  <article class="recordings-container">
		<span class="recordings-item" v-for="recording in recordings">
			<div v-if="recording.url">
				{{ recording.file }}<br>
				<audio v-bind:src="recording.url" controls="true"/><br>
				<a v-if="recording.url" v-bind:href="recording.url">download</a>
			</div>
			<div v-else>
				<a v-on:click="get_download_url(recording.file)">listen!</a>{{ recording.file }}<br>
			</div>
	  </span>
  </article>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PageContent',
	data () {
    return {
      recordings: null,
			download_links: [],
    }
  },
	methods: {
		set_recordings(recordings) {
			console.log(recordings)
			this.recordings = recordings
		},
		get_download_url(file) {
			axios
				.get('/dashboard/recordings/' + file)
				.then(response => (this.show_player(response.data.file_download)))
		},
		show_player(file_download){
			console.log(file_download)
			this.download_links.push(file_download)
			console.log(this.recordings)
			console.log(this.download_links)
			var x, y;
			for (x in this.download_links) {
				for (y in this.recordings) {
					if (this.download_links[x].file == this.recordings[y].file)
						this.recordings[y].url = this.download_links[x].url
						console.log("Match: " + this.download_links[x].url)
				}
			}
		}
	},
  mounted () {
    axios
      .get('/dashboard/recordings')
      .then(response => (this.set_recordings(response.data.recordings)))
  }
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.recordings-container {
	color: map-get($colors, "bright");
	max-height: 200px;
	overflow-y: scroll;
	a {cursor: pointer;}
}
</style>
