<template>
	<div class="api-container">
		<h2>JackTrip Settings</h2>
		<p>{{server_settings.jacktrip_q}}</p>
		<p>{{server_settings.jack_fpp}}</p>
		<div v-for="value in q_values">
			<button v-bind:class="{'active': server_settings.jacktrip_q == value}" v-on:click="set_q(value)">{{value}}</button>
		</div>
	</div>
</template>

<script>
import jsonrpc from 'jsonrpc-lite'
import axios from 'axios'

export default {
  name: 'DashboarApi',
	data () {
    return {
			q_values: ["4", "6", "8", "10", "12", "14", "16"],
			fpp_values: [64, 128, 256, 512],
			next_server_settings: {
				jack_fpp: null,
				jacktrip_q: null,
			},
      server_settings: {
				jack_fpp: null,
				jacktrip_q: null,
			}
    }
  },
	methods: {
		set_q(q_value){
			let requestObj = jsonrpc.request('1', 'set_q', {q_value: q_value})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_set_q(response)))
		},
		set_fpp(fpp_value){
			let requestObj = jsonrpc.request('1', 'set_fpp', {fpp_value: fpp_value})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_set_fpp(response)))
		},
		get_fpp(){
			let requestObj = jsonrpc.request('1', 'get_fpp')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_get_fpp(response)))
		},
		get_q(){
			let requestObj = jsonrpc.request('1', 'get_q')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_get_q(response)))
		},
		restart_jacktrip(){
			let requestObj = jsonrpc.request('1', 'restart_jacktrip')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_restart_jacktrip(response)))
		},
		restart_jackd(){
			let requestObj = jsonrpc.request('1', 'restart_jackd')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_restart_jackd(response)))
		},
		handle_get_fpp(response){
			// need error checking
			this.server_settings.jack_fpp = response.data.result
			this.next_server_settings.jack_fpp = response.data.result
		},
		handle_get_q(response){
			// need error checking
			this.server_settings.jacktrip_q = response.data.result
			this.next_server_settings.jacktrip_q = response.data.result
		},
		handle_set_q(response){
			// need error checking
			this.restart_jacktrip()
			this.get_q()
		},
		handle_set_fpp(response){
			// need error checking
			this.restart_jackd()
			this.get_fpp()
		},
		handle_restart_jacktrip(response){
			// need error checking
			console.log("JackTrip restarted with response:", response)
		},
		handle_restart_jackd(response){
			// need error checking
			console.log("JACKD restarted with response:", response)
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

.active {
	font-weight: bold;
}

</style>
