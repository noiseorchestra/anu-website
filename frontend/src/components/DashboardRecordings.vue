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
        <div class="recordings-item-content-child player" player>
          <audio :src="recording.url" controls="true" />
        </div>
        <div class="recordings-item-content-child button">
          <a :href="recording.url">download</a>
        </div>
      </div>
      <div v-else class="recordings-item-content no-player">
        <div class="recordings-item-content-child">
          <a href="#0" @click="getDownloadUrl(recording.file)">{{
            recording.dateTime
          }}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DashboardRecordings',
  data() {
    return {
      recordings: null,
      download_links: [],
    };
  },
  mounted() {
    axios
      .get('/dashboard/recordings')
      .then((response) =>
        this.setRecording(response.data.recordings),
      );
  },
  methods: {
    setRecording(recordings) {
      this.recordings = recordings;
      this.recordings.forEach((item, i) => {
        this.recordings[i].dateTime = this.getDateTime(item.file);
      });
    },
    getDownloadUrl(file) {
      axios
        .get('/dashboard/recordings/' + file)
        .then((response) =>
          this.showPlayer(response.data.fileDownload),
        );
    },
    showPlayer(fileDownload) {
      this.download_links.push(fileDownload);
      let x, y;
      for (x in this.download_links) {
        for (y in this.recordings) {
          if (
            this.download_links[x].file === this.recordings[y].file
          ) {
            this.recordings[y].url = this.download_links[x].url;
          }
        }
      }
    },
    getDateTime(fileString) {
      const dateString = fileString.split('-');
      const units = dateString[1].split('_');
      const date = new Date(
        units[0],
        units[1] - 1,
        units[2],
        units[3].slice(0, 2),
        units[3].slice(2, 4),
      );
      return date.toLocaleString();
    },
  },
};
</script>

<style scoped lang="scss">
@import '@/scss/_variables.scss';

a {
  font-weight: bold;
  font-family: map-get($font, 'main-family');
  padding-top: 0px;
}

.recordings-container {
  display: flex;
  flex-direction: column;
  color: map-get($colors, 'bright');
  overflow-y: scroll;
  height: 100%;
  width: 100%;
  a {
    cursor: pointer;
  }
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
