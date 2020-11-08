<template>
  <ul class="recordings-container">
		<li v-for="recording in recordings">
	    {{ recording }}
	  </li>
  </ul>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PageContent',
	data () {
    return {
      recordings: null
    }
  },
  mounted () {
    axios
      .get('/dashboard/recordings')
      .then(response => (this.recordings = response.data.recordings))
  }
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.recordings-container {
	li {color: white;}
}

</style>
