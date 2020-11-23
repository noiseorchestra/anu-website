<template>
	<div class="recordings-container">
		<h2>Recordings</h2>
		<div class="recordings-item" v-for="recording in recordings">
			<div class="recordings-item-content with-player">
				<div class="recordings-item-content-child player"><a v-bind:href="recording.link">{{recording.title}}</a><b></b></div>
				<div class="recordings-item-content-child date">{{recording.date}}</div>
				<div class="recordings-item-content-child info">{{recording.info}}</div>
			</div>
	  </div>
	</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ListenRecordings',
	data () {
    return {
      recordings: null,
    }
  },
	methods: {
		set_recordings(recordings) {
			recordings.forEach((recording, i) => {
				let date = new Date(recording.date)
				recordings[i].date = date.toLocaleDateString()
			});
			this.recordings = recordings
		},
	},
  mounted () {
    axios
      .get('/sounds/recordings')
      .then(response => (this.set_recordings(response.data)))
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
	flex-direction: column;
	flex: 1 1 auto;
	&.with-player {
		flex-wrap: wrap;
	}
}

.date {
	font-style: italic;
}

.recordings-item-content-child {
	flex: 0 1 auto;
}

</style>
