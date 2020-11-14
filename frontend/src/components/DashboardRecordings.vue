<template>
	<div class="recordings-container">
		<div class="recordings-item" v-for="recording in recordings">
			<div class="recordings-item-content with-player" v-if="recording.url">
				<div class="recordings-item-content-child player" player><audio v-bind:src="recording.url" controls="true"/></div>
				<div class="recordings-item-content-child button"><a v-bind:href="recording.url">download</a></div>
			</div>
			<div class="recordings-item-content no-player" v-else>
				<div class="recordings-item-content-child filename">{{ recording.file }}</div>
				<div class="recordings-item-content-child"><a href="#0" v-on:click="get_download_url(recording.file)">listen!</a></div>
			</div>
	  </div>
	</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DashboardRecordings',
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
			this.download_links.push(file_download)
			var x, y;
			for (x in this.download_links) {
				for (y in this.recordings) {
					if (this.download_links[x].file == this.recordings[y].file) {
						this.recordings[y].url = this.download_links[x].url
					}
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
	display: flex;
	flex-direction: column;
	color: map-get($colors, "bright");
	overflow-y: scroll;
	height: 100%;
	width: 100%;
	a {cursor: pointer;}
}

.recordings-item {
	display: flex;
	flex-direction: column;
	flex: 0 0 40px;
}

.recordings-item-content {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-between;
	flex: 1 1 auto;
	&.with-player {
		flex-wrap: wrap;
	}
}

.recordings-item-content-child {
	flex: 0 1 auto;
	// overflow-wrap: anywhere;
	// & .filename {
	// 	flex: 2 1 auto;
	// }
}

</style>
