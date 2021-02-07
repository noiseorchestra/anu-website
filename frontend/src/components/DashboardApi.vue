<template>
	<div class="api-container">
		<div class="current-info">
			<div><h2>JackTrip Hub Server Settings</h2></div>
			<div class="value-picker jacktrip-queue">
				<div class="key">JackTrip queue:</div>
				<div class="values">
					<div v-bind:class="{'deactivate': busy}" v-for="value in q_values">
						<button class="api-button" v-bind:class="{'selected': selected_server_settings.jacktrip_q == value}" v-on:click="set_q(value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="value-picker jack-fpp">
				<div class="key">JACK fpp:</div>
				<div class="values">
					<div v-bind:class="{'deactivate': busy}" v-for="value in fpp_values">
						<button class="api-button" v-bind:class="{'selected': selected_server_settings.jack_fpp == value}" v-on:click="set_fpp(value)">{{value}}</button>
					</div>
				</div>
			</div>
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
			busy: false,
			q_values: [4, 6, 8, 10, 12, 14, 16],
			fpp_values: [64, 128, 256, 512],
			selected_server_settings: {
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
			this.busy = true
			this.selected_server_settings.jacktrip_q = q_value
			let requestObj = jsonrpc.request('1', 'set_q', {q_value: q_value})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_set_q(response)))
		},
		set_fpp(fpp_value){
			this.busy = true
			this.selected_server_settings.jack_fpp = fpp_value
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
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				this.busy = true
				return
			}
			this.selected_server_settings.jack_fpp = response.data.result
			this.server_settings.jack_fpp = response.data.result
		},
		handle_get_q(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				this.busy = true
				return
			}
			this.selected_server_settings.jacktrip_q = response.data.result
			this.server_settings.jacktrip_q = response.data.result
		},
		handle_set_q(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				this.busy = true
				return
			}
			this.restart_jacktrip()
		},
		handle_set_fpp(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				this.busy = true
				return
			}
			this.restart_jackd()
		},
		handle_restart_jacktrip(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				this.busy = true
				return
			}
			this.get_q()
			this.busy = false
		},
		handle_restart_jackd(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				this.busy = true
				return
			}
			this.get_fpp()
			this.busy = false
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
@import "@/scss/_common.scss";
@include api-style;

.api-container{
	display: flex;
	flex-direction: column;
	color: map-get($colors, "bright");
	height: 100%;
}

.value-picker {
	display: flex;
	flex-direction: row;
}

.key {
	flex: 0 0 80px;
}

.values {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
}

</style>
