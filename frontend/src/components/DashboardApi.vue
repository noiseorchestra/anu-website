<template>
	<div v-bind:class="{'deactivate': server_call_in_progress}" class="api-container">
		<div class="current-info">
			<div><h2>JackTrip Hub Server Settings</h2></div>
			<div class="api-container-child jacktrip-queue">
				<div class="key">JackTrip queue: </div>
				<div class="values">
					<div v-bind:key="value" v-bind:class="{'deactivate': disabled}" v-for="value in q_values">
						<button class="api-button" v-bind:class="{'selected': server_settings.jacktrip_q == value}" v-on:click="set_q(ip, value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="api-container-child jack-fpp">
				<div class="key">JACK fpp: </div>
				<div class="values">
					<div v-bind:key="value" v-bind:class="{'deactivate': disabled}" v-for="value in fpp_values">
						<button class="api-button" v-bind:class="{'selected': server_settings.jack_fpp == value}" v-on:click="set_fpp(ip, value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="api-container-child server-details">
				<div class="key">Server IP: </div>
				<div class="values">
					<div v-if="ip">{{ip}}</div><div><button class="api-button" v-on:click="refresh_server_details()">refresh</button></div>
				</div>
			</div>
			<div class="api-container-child server-details">
				<div class="key">status: </div>
				<div v-bind:class="{'deactivate': disabled}" class="values">
					<div>{{server_status}}</div>
				</div>
			</div>
			<div class="api-container-child server-automation">
				<div class="key"></div>
				<div class="values">
					<div v-bind:class="{'deactivate': creating_server}">
						<button v-if="!ip" class="api-button" v-on:click="create_server()">new server</button>
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
			server_call_in_progress: false,
			server_status: "no server",
			ip: false,
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
			this._serverCallStarted()
			this.creating_server = true
			let requestObj = jsonrpc.request('1', 'create_server')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this._raise_error(response))
				.then(() => this._get_and_set_server_ip())
				.then(() => this._wait_for_ready(this.ip))
				.then(() => this._upload_scripts(this.ip))
				.then(() => this._handleServerCreateSuccess())
				.catch(response => this._handleServerCallError(response))
				.finally(() => this._handleServerCallFinally())
		},
		delete_server(){
			this._serverCallStarted()
			let requestObj = jsonrpc.request('1', 'delete_all_servers')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this._raise_error(response)))
				.then(() => this._handleServerDeleteSuccess())
				.catch(response => this._handleServerCallError(response))
				.finally(response => this._handleServerCallFinally(response))
		},
		refresh_server_details(){
			this._serverCallStarted()
			this._get_and_set_server_ip()
			.then(() => this._get_server_status(this.ip))
			.then(() => this._get_fpp(this.ip))
			.then(() => this._get_q(this.ip))
			.then(() => this._handleServerCallSuccess())
			.catch(response => this._handleServerCallError(response))
			.finally(() => this._handleServerCallFinally())
		},
		set_q(host, q_value){
			this._serverCallStarted()
			let requestObj = jsonrpc.request('1', 'set_q', {host: host, q_value: q_value})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this._raise_error(response)))
				.then(() => this._restart_jacktrip(host))
				.then(() => this._get_q(host))
				.then(() => this._handleServerCallSuccess())
				.catch(response => this._handleServerCallError(response))
				.finally(() => this._handleServerCallFinally())
		},
		set_fpp(host, fpp_value){
			this._serverCallStarted()
			let requestObj = jsonrpc.request('1', 'set_fpp', {host: host, fpp_value: fpp_value})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this._raise_error(response)))
				.then(() => this._restart_jackd(host))
				.then(() => this._get_fpp(host))
				.then(() => this._handleServerCallSuccess())
				.catch(response => this._handleServerCallError(response))
				.finally(() => this._handleServerCallFinally())
		},
		_wait_for_ready(host){
			const whileLoop = async (host) => {
				let response, status, count = 0;
				while (status !== "running") {
					count++;
					status = await this._get_server_status(host)
					if (count === 20) {
						throw new Error("Timeout, waited too long for server to boot.");
					}
					await new Promise(r => setTimeout(r, 5000));
				}
				// Extra wait as port 22 doesn't seem to be open straight away
				this.server_status += " (waiting)"
				await new Promise(r => setTimeout(r, 60000));
				return response
			}
			return whileLoop(host)
		},
		_upload_scripts(host){
			this.server_status = "installing dependencies (will take approx. 10mins)"
			let requestObj = jsonrpc.request('1', 'upload_scripts', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this._raise_error(response))
				.then(() => setTimeout(() => {
					this.server_status = "rebooting"
				}, 60000))
		},
		_get_and_set_server_ip(){
			let requestObj = jsonrpc.request('1', 'fetch_all_servers')
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => {
					this._raise_error(response)
					this.ip = response.data.result.ip
					return response.data.result.ip})
		},
		_get_server_status(host){
			let requestObj = jsonrpc.request('1', 'get_server_status', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this._raise_error(response))
				.then(response => {
					this.server_status = response.data.result.status
					return response.data.result.status})
		},
		_get_fpp(host){
			let requestObj = jsonrpc.request('1', 'get_fpp', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this._raise_error(response))
				.then(response => {this.server_settings.jack_fpp = response.data.result.value})
		},
		_get_q(host){
			let requestObj = jsonrpc.request('1', 'get_q', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this._raise_error(response))
				.then(response => {this.server_settings.jacktrip_q = response.data.result.value})
		},
		_restart_jacktrip(host){
			let requestObj = jsonrpc.request('1', 'restart_jacktrip', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this._raise_error(response)))
		},
		_restart_jackd(host){
			let requestObj = jsonrpc.request('1', 'restart_jackd', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this._raise_error(response)))
		},
		_raise_error(response){
			if (response.data.error){
				throw new Error(response.data.error.message);
			}
			return response
		},
		_handleServerCallSuccess(){
			this.server_ready = true
			this.disabled = false
		},
		_handleServerCreateSuccess(){
			this.server_ready = true
			this.refresh_server_details()
		},
		_handleServerDeleteSuccess(){
			this.server_ready = false
			this.ip = false
			this.disabled = true
			this.server_status = "no server"
		},
		_handleServerCallFinally(){
			this.creating_server = false
			this.server_call_in_progress = false
		},
		_handleServerCallError(response){
			window.alert(response)
			this.server_status += " (error)"
		},
		_serverCallStarted(){
			this.server_call_in_progress = true
			this.disabled = true
		}
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
