<template>
	<div class="api-container">
	</div>
</template>

<script>
import jsonrpc from 'jsonrpc-lite'
import axios from 'axios'

export default {
  name: 'DashboarApi',
  mounted () {
		const requestObj = jsonrpc.request('1', 'add', {a: 1, b: 2})
    axios
      .post('/dashboard/rpc/', requestObj)
      .then(response => (console.log(response)))
  }
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

</style>
