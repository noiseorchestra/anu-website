<template>
	<div class="api-container">
		<h2>JackTrip Settings</h2>
		<p>{{server_settings.jacktrip_q}}</p>
		<p>{{server_settings.jack_fpp}}</p>
	</div>
</template>

<script>
import jsonrpc from 'jsonrpc-lite'
import axios from 'axios'

export default {
  name: 'DashboarApi',
	data () {
    return {
      server_settings: {
				jack_fpp: null,
				jacktrip_q: null,
			}
    }
  },
	methods: {
		get_fpp(){
			let requestObj = jsonrpc.request('1', 'get_fpp')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_fpp(response)))
		},
		get_q(){
			let requestObj = jsonrpc.request('1', 'get_q')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_q(response)))
		},
		handle_fpp(response){
			this.server_settings.jack_fpp = response.data.result
		},
		handle_q(response){
			this.server_settings.jacktrip_q = response.data.result
		},
	},
  mounted () {
		this.get_fpp()
		this.get_q()
  }
}
</script>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.api-container{
	height: 20px;
	color: white;
}

</style>
