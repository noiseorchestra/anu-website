<template>
  <div class="recordings-container">
    <h2>Recordings</h2>
    <div
      v-for="recording in recordings"
      :key="recording.url"
      class="recordings-item"
    >
      <div
        v-if="recording.url"
        class="recordings-item-content with-player"
      >
        <div
          class="recordings-item-content-child player"
          player
        >
          <audio
            :src="recording.url"
            controls="true"
          />
        </div>
        <div class="recordings-item-content-child button">
          <a :href="recording.url">download</a>
        </div>
      </div>
      <div
        v-else
        class="recordings-item-content no-player"
      >
        <div class="recordings-item-content-child">
          <a
            href="#0"
            @click="get_download_url(recording.file)"
          >{{ recording.dateTime }}</a>
        </div>
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
  mounted () {
    axios
      .get('/dashboard/recordings')
      .then(response => (this.set_recordings(response.data.recordings)))
  },
	methods: {
		set_recordings(recordings) {
			this.recordings = recordings
			this.recordings.forEach((item, i) => {
				this.recordings[i].dateTime = this.get_date_time(item.file)
			});
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
		},
		get_date_time(file_string){
			let date_string = file_string.split("-")
			let units = date_string[1].split("_")
			let date = new Date(units[0], units[1] - 1, units[2], units[3].slice(0, 2), units[3].slice(2, 4))
			console.log(date.toLocaleString())
			return date.toLocaleString()
		}
	}
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

a {
  font-weight: bold;
  font-family: map-get($font, "main-family");
  padding-top: 0px;
}

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
