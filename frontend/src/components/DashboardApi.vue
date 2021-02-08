<template>
	<div class="api-container">
		<div class="current-info">
			<div><h2>JackTrip Hub Server Settings</h2></div>
			<div class="api-container-child jacktrip-queue">
				<div class="key">JackTrip queue:</div>
				<div class="values">
					<div v-bind:class="{'deactivate': disabled}" v-for="value in q_values">
						<button class="api-button" v-bind:class="{'selected': server_settings.jacktrip_q == value}" v-on:click="set_q(value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="api-container-child jack-fpp">
				<div class="key">JACK fpp:</div>
				<div class="values">
					<div v-bind:class="{'deactivate': disabled}" v-for="value in fpp_values">
						<button class="api-button" v-bind:class="{'selected': server_settings.jack_fpp == value}" v-on:click="set_fpp(value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="api-container-child server-details">
				<div class="key">Server IP:</div>
				<div v-bind:class="{'deactivate': disabled}" class="values">
					<div>{{ip}}</div><div><button class="api-button" v-on:click="refresh_server_details()">refresh</button></div>
				</div>
			</div>
			<div class="api-container-child server-automation">
				<div class="key">Servers:</div>
				<div class="values">
					<div v-bind:class="{'deactivate': creating_server}">
						<button v-if="!server_ready" class="api-button" v-on:click="create_server()">new server</button>
						<button v-else class="api-button" v-on:click="delete_server()">delete server</button>
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
			disabled: true,
			creating_server: true,
			server_ready: false,
			ip: "",
			server_settings: {
				jack_fpp: null,
				jacktrip_q: null,
			},
			q_values: [4, 6, 8, 10, 12, 14, 16],
			fpp_values: [64, 128, 256, 512],
		}
	},
	methods: {
		create_server(){
			this.disabled = true
			this.creating_server = true
			let requestObj = jsonrpc.request('1', 'create_server')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this.handle_error(response))
				.then(response => this.ip = response.data.result.ip)
				.then(() => this.wait_for_ready())
				.then(() => this.upload_scripts())
				.then(() => {this.server_ready = true})
				.catch(response => window.alert(response))
				.finally(() => {
					this.creating_server = false
					this.disabled = false
				})
		},
		wait_for_ready(host){
			const whileLoop = async (host) => {
				let response, status, count = 0;
				while (status !== "running") {
					count++;
					response = await this.get_server_status(host)
					status = response.data.result.status
					if (count === 20) {
						throw new Error("Timeout, waited too long for server to boot. ", response);
					}
					await new Promise(r => setTimeout(r, 5000));
				}
				// Extra wait as port 22 doesn't seem to be open straight away
				await new Promise(r => setTimeout(r, 60000));
				return response
			}
			return whileLoop(this.ip)
		},
		upload_scripts(){
			let requestObj = jsonrpc.request('1', 'upload_scripts', {host: this.ip})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this.handle_error(response))
		},
		refresh_server_details(){
			this.disabled = true
			this.get_server_ip()
			.then(response => this.get_fpp())
			.then(response => this.get_q())
			.then(response => {
				this.disabled = false
				this.creating_server = false
				this.server_ready = true})
			.catch(response => window.alert(response))
		},
		get_server_ip(){
			let requestObj = jsonrpc.request('1', 'fetch_all_servers')
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => {
					this.handle_error(response)
					this.ip = response.data.result.ip})
		},
		get_server_status(host){
			let requestObj = jsonrpc.request('1', 'get_server_status', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this.handle_error(response))
		},
		get_fpp(){
			console.log()
			let requestObj = jsonrpc.request('1', 'get_fpp', {host: this.ip})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this.handle_error(response))
				.then(response => {
					this.server_settings.jack_fpp = response.data.result.value
					return response
				})
		},
		get_q(){
			let requestObj = jsonrpc.request('1', 'get_q', {host: this.ip})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this.handle_error(response))
				.then(response => {
					this.server_settings.jacktrip_q = response.data.result.value
					return response
				})
		},
		set_q(q_value){
			this.disabled = true
			let requestObj = jsonrpc.request('1', 'set_q', {host: this.ip, q_value: q_value})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_error(response)))
				.then(() => this.restart_jacktrip())
				.then(() => this.get_q())
				.then(() => {this.disabled = false})
				.catch(response => window.alert(response))
		},
		set_fpp(fpp_value){
			this.disabled = true
			let requestObj = jsonrpc.request('1', 'set_fpp', {host: this.ip, fpp_value: fpp_value})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_error(response)))
				.then(() => this.restart_jackd())
				.then(() => this.get_fpp())
				.then(() => {this.disabled = false})
				.catch(response => window.alert(response))
		},
		restart_jacktrip(){
			let requestObj = jsonrpc.request('1', 'restart_jacktrip', {host: this.ip})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_error(response)))
		},
		restart_jackd(){
			let requestObj = jsonrpc.request('1', 'restart_jackd', {host: this.ip})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_error(response)))
		},
		delete_server(){
			let requestObj = jsonrpc.request('1', 'delete_all_servers')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_error(response)))
		},
		handle_error(response){
			if (response.data.error){
				throw new Error(response.data.error.message);
			}
			return response
		},
	},
  mounted () {
		this.refresh_server_details()
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

.api-container-child {
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
