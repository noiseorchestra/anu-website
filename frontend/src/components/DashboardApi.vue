<template>
	<div v-bind:class="{'deactivate': serverCallInProgress}" class="api-container">
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
			rpc_count: 0,
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
	computed: {
    // a computed getter
		serverCallInProgress: function () {
		// `this` points to the vm instance
		return this.rpc_count != 0;
		}
  	},
  	methods: {
		// create_server(){
		// 	this.onStartRPC()
		// 	this.creating_server = true
		// 	let requestObj = jsonrpc.request('1', 'create_server')
		// 	// make "create_server" post call to RPC API
		// 	axios
		// 		.post('/dashboard/rpc/', requestObj)
		// 		// check response for error
		// 		.then(response => this.checkForError(response))
		// 		// perform follow up tasks
		// 		// .then(() => this.getAndSetServerIP())
		// 		// .then(() => this.waitForReady(this.ip))
		// 		// .then(() => this.uploadScripts(this.ip))
		// 		// handle succesful completion
		// 		.then(() => this.handleServerCreateSuccess())
		// 		// catch errors
		// 		.catch(response => this.handleServerCallError(response))
		// 		// execute in all situations
		// 		.finally(() => this.handleServerCallFinally())
		// },
		async fetchServerDetails () {
			try {
				let host = await this.getServerIP()
				let fpp = await this.getFpp(host)
				let q = await this.getQ(host)
				this.ip = host
				this.fpp = fpp
				this.q = q
			} catch (e) {
				handleServerCallError(e)
			} finally {
				console.log('Finally!');
			}
		},
		createServer(){
			let requestObj = jsonrpc.request('1', 'create_server')
			return this.executeRPC(requestObj)
		},
		waitForReady(host){
			const whileLoop = async (host) => {
				let response, status, count = 0;
				while (status !== "running") {
					count++;
					// this needs adapting to new return object
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
		// uploadScripts(host){
		// 	// this needs refactoring too
		// 	this.server_status = "installing dependencies (will take approx. 10mins)"
		// 	let requestObj = jsonrpc.request('1', 'upload_scripts', {host: host})
		// 	return axios
		// 		.post('/dashboard/rpc/', requestObj)
		// 		.then(response => this.checkForError(response))
		// 		.then(() => setTimeout(() => {
		// 			this.server_status = "rebooting"
		// 		}, 60000))
		// },
		uploadScripts(host){
			let requestObj = jsonrpc.request('1', 'upload_scripts', {host: host})
			return this.executeRPC(requestObj)		
		},
		deleteServer(){
			let requestObj = jsonrpc.request('1', 'delete_all_servers')
			return this.executeRPC(requestObj)		
		},
		setQ(host, q_value){
			let requestObj = jsonrpc.request('1', 'set_q', {host: host, q_value: q_value})
			return this.executeRPC(requestObj)		
		},
		setFpp(host, fpp_value){
			let requestObj = jsonrpc.request('1', 'set_fpp', {host: host, fpp_value: fpp_value})
			return this.executeRPC(requestObj)		
		},
		getServerIP(){
			let requestObj = jsonrpc.request('1', 'fetch_all_servers')
			return this.executeRPC(requestObj)
		},
		getServerStatus(host){
			let requestObj = jsonrpc.request('1', 'get_server_status', {host: host})
			return this.executeRPC(requestObj)
		},
		getFpp(host){
			let requestObj = jsonrpc.request('1', 'get_fpp', {host: host})
			return this.executeRPC(requestObj)
		},
		getQ(host){
			let requestObj = jsonrpc.request('1', 'get_q', {host: host})
			return this.executeRPC(requestObj)
		},
		restartJackTrip(host){
			let requestObj = jsonrpc.request('1', 'restart_jacktrip', {host: host})
			return this.executeRPC(requestObj)
		},
		restartJack(host){
			let requestObj = jsonrpc.request('1', 'restart_jackd', {host: host})
			return executeRPC(requestObj)
		},
		executeRPC(requestObj){
			this.onStartRPC()
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.checkForError(response)))
				.then(response => {return response.data.result})
				.catch(response => handleServerCallError(response))
				.finally(() => this.onFinishRPC())
		},
		checkForError(response){
			if (response.data.error){
				throw new Error(response.data.error.message);
			}
			return response
		},
		// handleServerCallSuccess(){
		// 	this.server_ready = true
		// 	this.disabled = false
		// },
		// handleServerCreateSuccess(){
		// 	this.server_ready = true
		// 	// this.refreshServerDetails()
		// },
		// handleServerDeleteSuccess(){
		// 	this.server_ready = false
		// 	this.ip = false
		// 	this.disabled = true
		// 	this.server_status = "no server"
		// },
		// handleServerCallFinally(){
		// 	this.creating_server = false
		// 	this.server_call_in_progress = false
		// },
		// handleServerCallError(response){
		// 	window.alert(response)
		// 	this.server_status += " (error)"
		// },
		onStartRPC(){
			this.rpc_count += 1
		},
		onFinishRPC(){
			this.rpc_count -= 1
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
