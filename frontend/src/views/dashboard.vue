<template>
  <main>
    <div class="dashboard grid">
  		<div class="grid-item info"><DashboardInfo :naw="naw"></DashboardInfo></div>
      <div class="grid-item stream"><DashboardStream/></div>
  		<div class="grid-item recordings"><DashboardRecordings/></div>
      <div class="grid-item api"><DashboardApi/></div>
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
  name: 'page',
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
  padding: 30px;
  grid-gap: 30px;
  grid-template-columns: repeat(2, 1fr);
  grid-auto-rows: 135px;
}

.info {
  grid-row: 1/3;
}

.recordings {
  grid-row: 1/5;
  min-width: 330px;
}

.grid-item {
  outline: 3px dashed red;
  padding: 2px;
  overflow-y: auto;
}

</style>
