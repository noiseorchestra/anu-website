<template>
  <div class="stream-events-container">
    <h2>Upcomming Live-Streams</h2>
    <div
      v-for="event in events"
      :key="event.date"
      class="stream-events-item"
    >
      <div class="stream-events-item-content with-player">
        <div class="stream-events-item-content-child player">
          <a :href="event.link">{{ event.title }}</a><b />
        </div>
        <div class="stream-events-item-content-child date">
          {{ event.date }}
        </div>
        <div class="stream-events-item-content-child info">
          {{ event.info }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ListenStreamEvents',
	data () {
    return {
      events: null,
    }
  },
  mounted () {
    axios
      .get('/sounds/events')
      .then(response => (this.set_stream_events(response.data)))
  },
	methods: {
		set_stream_events(events) {
			events.forEach((event, i) => {
				let date = new Date(event.date)
				events[i].date = date.toLocaleString()
			});
			this.events = events
		},
	}
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.stream-events-container {
	display: flex;
	flex-direction: column;
	color: map-get($colors, "bright");
	overflow-y: scroll;
	height: 100%;
	width: 100%;
	a {cursor: pointer;}
}

.stream-events-item {
	display: flex;
	flex-direction: column;
	flex: 0 0 40px;
}

.stream-events-item-content {
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

.stream-events-item-content-child {
	flex: 0 1 auto;
}

</style>
