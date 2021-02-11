<template>
	<div v-bind:class="{'deactivate': server_call_in_progress}" class="api-container">
		<div class="current-info">
			<div><h2>JackTrip Hub Server Settings</h2></div>
			<div class="api-container-child jacktrip-queue">
				<div class="key">JackTrip queue: </div>
				<div class="values">
					<div v-bind:key="value" v-bind:class="{'deactivate': disabled}" v-for="value in q_values">
						<button class="api-button" v-bind:class="{'selected': server_settings.jacktrip_q == value}" v-on:click="setQ(ip, value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="api-container-child jack-fpp">
				<div class="key">JACK fpp: </div>
				<div class="values">
					<div v-bind:key="value" v-bind:class="{'deactivate': disabled}" v-for="value in fpp_values">
						<button class="api-button" v-bind:class="{'selected': server_settings.jack_fpp == value}" v-on:click="setFpp(ip, value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="api-container-child server-details">
				<div class="key">Server IP: </div>
				<div class="values">
					<div v-if="ip">{{ip}}</div><div><button class="api-button" v-on:click="refreshServerDetails()">refresh</button></div>
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
	name: 'DashboardApi',
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
			this.serverCallStarted()
			this.creating_server = true
			let requestObj = jsonrpc.request('1', 'create_server')
			// make "create_server" post call to RPC API
			axios
				.post('/dashboard/rpc/', requestObj)
				// check response for error
				.then(response => this.checkForError(response))
				// perform follow up tasks
				.then(() => this.getAndSetServerIP())
				.then(() => this.waitForReady(this.ip))
				.then(() => this.uploadScripts(this.ip))
				// handle succesful completion
				.then(() => this.handleServerCreateSuccess())
				// catch errors
				.catch(response => this.handleServerCallError(response))
				// execute in all situations
				.finally(() => this.handleServerCallFinally())
		},
		refreshServerDetails(){
			this.serverCallStarted()
			this.getAndSetServerIP()
				.then(() => this.getServerStatus(this.ip))
				.then(() => this.getFpp(this.ip))
				.then(() => this.getQ(this.ip))
				.then(() => this.handleServerCallSuccess())
				.catch(response => this.handleServerCallError(response))
				.finally(() => this.handleServerCallFinally())
		},
		waitForReady(host){
			const whileLoop = async (host) => {
				let response, status, count = 0;
				while (status !== "running") {
					count++;
					status = await this.getServerStatus(host)
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
		uploadScripts(host){
			this.server_status = "installing dependencies (will take approx. 10mins)"
			let requestObj = jsonrpc.request('1', 'upload_scripts', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this.checkForError(response))
				.then(() => setTimeout(() => {
					this.server_status = "rebooting"
				}, 60000))
		},
		delete_server(){
			this.serverCallStarted()
			let requestObj = jsonrpc.request('1', 'delete_all_servers')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.checkForError(response)))
				.then(() => this.handleServerDeleteSuccess())
				.catch(response => this.handleServerCallError(response))
				.finally(response => this.handleServerCallFinally(response))
		},
		setQ(host, q_value){
			this.serverCallStarted()
			let requestObj = jsonrpc.request('1', 'set_q', {host: host, q_value: q_value})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.checkForError(response)))
				.then(() => this.restartJackTrip(host))
				.then(() => this.getQ(host))
				.then(() => this.handleServerCallSuccess())
				.catch(response => this.handleServerCallError(response))
				.finally(() => this.handleServerCallFinally())
		},
		setFpp(host, fpp_value){
			this.serverCallStarted()
			let requestObj = jsonrpc.request('1', 'set_fpp', {host: host, fpp_value: fpp_value})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.checkForError(response)))
				.then(() => this.restartJack(host))
				.then(() => this.getFpp(host))
				.then(() => this.handleServerCallSuccess())
				.catch(response => this.handleServerCallError(response))
				.finally(() => this.handleServerCallFinally())
		},
		getAndSetServerIP(){
			let requestObj = jsonrpc.request('1', 'fetch_all_servers')
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this.checkForError(response))
				.then(response => {
					this.ip = response.data.result.ip
					return response.data.result.ip})
				.catch(response => this.handleServerCallError(response))
		},
		getServerStatus(host){
			let requestObj = jsonrpc.request('1', 'get_server_status', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this.checkForError(response))
				.then(response => {
					this.server_status = response.data.result.status
					return response.data.result.status})
		},
		getFpp(host){
			let requestObj = jsonrpc.request('1', 'get_fpp', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this.checkForError(response))
				.then(response => {this.server_settings.jack_fpp = response.data.result.value})
		},
		getQ(host){
			let requestObj = jsonrpc.request('1', 'get_q', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => this.checkForError(response))
				.then(response => {this.server_settings.jacktrip_q = response.data.result.value})
		},
		restartJackTrip(host){
			let requestObj = jsonrpc.request('1', 'restart_jacktrip', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.checkForError(response)))
		},
		restartJack(host){
			let requestObj = jsonrpc.request('1', 'restart_jackd', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.checkForError(response)))
		},
		checkForError(response){
			console.log(response)
			if (response.data.error){
				throw new Error(response.data.error.message);
			}
			return response
		},
		handleServerCallSuccess(){
			this.server_ready = true
			this.disabled = false
		},
		handleServerCreateSuccess(){
			this.server_ready = true
			this.refreshServerDetails()
		},
		handleServerDeleteSuccess(){
			this.server_ready = false
			this.ip = false
			this.disabled = true
			this.server_status = "no server"
		},
		handleServerCallFinally(){
			this.creating_server = false
			this.server_call_in_progress = false
		},
		handleServerCallError(response){
			window.alert(response)
			this.server_status += " (error)"
		},
		serverCallStarted(){
			this.server_call_in_progress = true
			this.disabled = true
		}
	},
  mounted () {
		// this.refreshServerDetails()
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
