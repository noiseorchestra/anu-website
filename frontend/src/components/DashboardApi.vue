<template>
	<div v-bind:class="{'deactivate': disabled}" class="api-container">
		<div class="current-info">
			<div><h2>JackTrip Hub Server Settings</h2></div>
			<div class="api-container-child jacktrip-queue">
				<div class="key">JackTrip queue: </div>
				<div class="values">
					<div v-bind:key="value" v-bind:class="{'deactivate': disabled}" v-for="value in qValues">
						<button class="api-button" v-bind:class="{'selected': q == value}" v-on:click="setQ(ip, value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="api-container-child jack-fpp">
				<div class="key">JACK fpp: </div>
				<div class="values">
					<div v-bind:key="value" v-bind:class="{'deactivate': disabled}" v-for="value in fppValues">
						<button class="api-button" v-bind:class="{'selected': fpp == value}" v-on:click="setFpp(ip, value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="api-container-child server-details">
				<div class="key">Server IP: </div>
				<div class="values">
					<div v-if="ip">{{ip}}</div><div><button class="api-button" v-on:click="fetchServerIp()">refresh</button></div>
				</div>
			</div>
			<div class="api-container-child server-details">
				<div class="key">status: </div>
				<div v-bind:class="{'deactivate': disabled}" class="values">
					<div>{{serverStatus}}</div>
				</div>
			</div>
			<div class="api-container-child server-automation">
				<div class="key"></div>
				<div class="values">
					<div>
						<button v-if="!ip" class="api-button" v-on:click="initServer()">new server</button>
						<button v-else class="api-button" v-on:click="deleteServer()">delete server</button>
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
			rpcCount: 0,
			serverStatus: "no server",
			ip: null,
			q: null,
			fpp: null,
			qValues: [4, 6, 8, 10, 12, 14, 16],
			fppValues: [64, 128, 256, 512],
		}
	},
	computed: {
		// a computed getter
		disabled: function () {
		// `this` points to the vm instance
		return this.rpcCount != 0;
		}
  	},
  	methods: {
		async initServer () {
			// create the server
			let host = await this.createServer()
			// wait for server to boot
			await this.waitForReady(host)
			// extra wait to be safe
			this.serverStatus += " (waiting)"
			await new Promise(r => setTimeout(r, 60000));
			this.serverStatus = "installing dependencies (will take approx. 10mins)"
			await this.uploadScripts(host)
			// extra wait while rebooting
			await new Promise(r => setTimeout(r, 60000));
			await this.fetchServerDetails(host)
		},
		async fetchServerIp(){
			this.ip = await this.getServerIP()
		},
		async fetchServerDetails (host) {
			try {
				let fpp = await this.getFpp(host)
				let q = await this.getQ(host)
				this.fpp = fpp
				this.q = q
			} catch (e) {
				this.handleServerCallError(e)
			} finally {
				console.log('Finally!');
			}
		},
		async waitForReady (host, interval=5000, attempts=20) {
			let response, count = 0;
			while (response !== "running") {
				count++;
				console.log(host)
				response = await this.getServerStatus(host)
				this.serverStatus = response
				if (count == attempts) {
					console.log("ERROR")
					throw new Error("Timeout, waited too long for server to boot.");
				}
				await new Promise(r => setTimeout(r, interval));
			}
			return response
		},
		createServer(){
			let requestObj = jsonrpc.request('1', 'create_server')
			return this.executeRPC(requestObj)
		},
		uploadScripts(host){
			let requestObj = jsonrpc.request('1', 'upload_scripts', {host: host})
			return this.executeRPC(requestObj)
		},
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
			return this.executeRPC(requestObj)
		},
		executeRPC(requestObj){
			this.onStartRPC()
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.checkForError(response)))
				.then(response => {
					console.log(response)
					return response.data.result})
				.catch(response => this.handleServerCallError(response))
				.finally(() => this.onFinishRPC())
		},
		checkForError(response){
			if (response.data.error){
				throw new Error(response.data.error.message);
			}
			return response
		},
		// handleServerCallSuccess(){
		// 	this.serverReady = true
		// 	this.disabled = false
		// },
		// handleServerCreateSuccess(){
		// 	this.serverReady = true
		// 	// this.refreshServerDetails()
		// },
		// handleServerDeleteSuccess(){
		// 	this.serverReady = false
		// 	this.ip = false
		// 	this.disabled = true
		// 	this.server_status = "no server"
		// },
		// handleServerCallFinally(){
		// 	this.creatingServer = false
		// 	this.server_call_in_progress = false
		// },
		handleServerCallError(response){
			window.alert(response)
			this.server_status += " (error)"
		},
		onStartRPC(){
			this.rpcCount += 1
		},
		onFinishRPC(){
			this.rpcCount -= 1
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
