<template>
  <div class="listen-wrapper">
    <div class="listen grid">
  		<div class="grid-item recordings"><ListenRecordings/></div>
      <div class="grid-item upcomming"><ListenStreamEvents/></div>
  		<div class="grid-item stream"><DashboardStream/></div>
      <!-- <img src="../assets/anu-background-transparent.png"> -->
    </div>
  </div>
</template>

<script>
import ListenRecordings from '@/components/ListenRecordings.vue'
import ListenStreamEvents from '@/components/ListenStreamEvents.vue'
import DashboardStream from '@/components/DashboardStream.vue'

export default {
  name: 'page',
  components: {
		ListenRecordings,
		ListenStreamEvents,
		DashboardStream,
  },
}
</script>

<style scoped lang="scss">
@import "../scss/_variables.scss";

.listen-wrapper {
	min-width: 100vw;
	height: 100vh;
	overflow-y: auto;
}

.grid {
  display: grid;
  padding: 10px;
  padding-top: 40px;
  grid-gap: 30px;
  grid-template-columns: repeat(1, 100%);
  grid-auto-rows: 150px;
}

.recordings {
  grid-row: 1/3;
	grid-column: 2;
}

.upcoming {
  grid-row: 3/5;
}

.grid-item {
  outline: 3px solid map-get($colors, "bright");;
  padding: 2px;
  overflow-y: auto;
	background-color: black;
}

@media (min-width: map-get($breakpoints, "medium")) {
	.grid {
    grid-template-columns: repeat(2, 1fr);
    grid-auto-rows: 40vh;
    padding: 30px;
    padding-top: 40px;
	}
  .grid-item {
    padding: 10px;
  }
  .upcoming {
    grid-row: 1/3;
    min-width: 330px;
  }
}


</style>
