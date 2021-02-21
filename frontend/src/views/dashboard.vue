<template>
  <main>
    <div class="dashboard grid">
      <div class="grid-item info">
        <DashboardInfo :naw="naw" />
      </div>
      <div class="grid-item stream">
        <DashboardStream />
      </div>
      <div class="grid-item recordings">
        <DashboardRecordings />
      </div>
      <div class="grid-item api">
        <DashboardApi />
      </div>
      <!-- <img src="../assets/anu-background-transparent.png"> -->
    </div>
  </main>
</template>

<script>
import DashboardInfo from '@/components/DashboardInfo.vue'
import DashboardStream from '@/components/DashboardStream.vue'
import DashboardRecordings from '@/components/DashboardRecordings.vue'
import DashboardApi from '@/components/DashboardApi.vue'

export default {
  name: 'Page',
  components: {
    DashboardInfo,
    DashboardStream,
		DashboardRecordings,
    DashboardApi
  },
	props: {naw: Object},
}
</script>

<style scoped lang="scss">
@import "../scss/_variables.scss";

.grid {
  display: grid;
  padding: 10px;
  padding-top: 40px;
  grid-gap: 30px;
  grid-template-columns: repeat(1, 100%);
  grid-auto-rows: 150px;
}

.info {
  grid-row: 1/3;
}

.recordings {
  grid-row: 3/5;
}

.grid-item {
  outline: 3px solid map-get($colors, "bright");;
  padding: 2px;
  overflow-y: auto;
}

@media (min-width: map-get($breakpoints, "medium")) {
	.grid {
    grid-template-columns: repeat(2, 1fr);
    grid-auto-rows: 160px;
    padding: 30px;
    padding-top: 40px;
	}
  .grid-item {
    padding: 10px;
  }
  .recordings {
    grid-row: 1/3;
    min-width: 330px;
  }
}


</style>
