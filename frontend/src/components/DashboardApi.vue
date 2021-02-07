<template>
	<div class="api-container">
		<div class="current-info">
			<div><h2>JackTrip Hub Server Settings</h2></div>
			<div class="api-container-child jacktrip-queue">
				<div class="key">JackTrip queue:</div>
				<div class="values">
					<div v-bind:class="{'deactivate': busy}" v-for="value in q_values">
						<button class="api-button" v-bind:class="{'selected': selected_server_settings.jacktrip_q == value}" v-on:click="set_q(ip, value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="api-container-child jack-fpp">
				<div class="key">JACK fpp:</div>
				<div class="values">
					<div v-bind:class="{'deactivate': busy}" v-for="value in fpp_values">
						<button class="api-button" v-bind:class="{'selected': selected_server_settings.jack_fpp == value}" v-on:click="set_fpp(ip, value)">{{value}}</button>
					</div>
				</div>
			</div>
			<div class="api-container-child server-details">
				<div class="key">Server IP:</div>
				<div class="values">
					<div>{{ip}}</div><div><button class="api-button" v-on:click="get_server_ip()">refresh</button></div>
				</div>
			</div>
			<div class="api-container-child server-automation">
				<div class="key">Servers:</div>
				<div class="values">
					<div><button class="api-button" v-on:click="create_server()">new server</button></div>
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
			ip: "",
			server_settings: {
				jack_fpp: null,
				jacktrip_q: null,
			},
			q_values: [4, 6, 8, 10, 12, 14, 16],
			fpp_values: [64, 128, 256, 512],
			selected_server_settings: {
				jack_fpp: null,
				jacktrip_q: null,
			},
		}
	},
	methods: {
		create_server(){
			this.busy = true
			let requestObj = jsonrpc.request('1', 'create_server')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_create_server(response)))
				.then(response => (this.wait_for_ready(response.data.result.ip)))
				.then(response => (this.upload_scripts(response.data.result.ip)))
				.then(response => {console.log("Success: ", response)})
				.catch((response)=>{console.log("Error: ", response)})
		},
		wait_for_ready(host){
			console.log(host)
			const whileLoop = async (host) => {
				let response, status, count = 0;
				while (status !== "running") {
					count++;
					response = await this.get_server_status(host)
					status = response.data.result.status
					console.log(response)
					if (count === 20) {
						throw new Error("Timeout, waited too long for server to boot. ", response);
					}
					await new Promise(r => setTimeout(r, 5000));
				}
				// Extra wait as port 22 doesn't seem to be open straight away
				await new Promise(r => setTimeout(r, 60000));
				return response
				
			}
			return whileLoop(host)
		},
		upload_scripts(host){
			let requestObj = jsonrpc.request('1', 'upload_scripts', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
		},
		get_server_ip(){
			this.busy = true
			let requestObj = jsonrpc.request('1', 'fetch_all_servers')
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_get_server_ip(response)))
				.then(response => (this.get_fpp(response.data.result.ip)))
				.then(response => (this.get_q(response.data.result.ip)))
				.catch(response => {console.log("Error: ", response)})
		},
		get_server_status(host){
			this.busy = true
			let requestObj = jsonrpc.request('1', 'get_server_status', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
		},
		set_q(host, q_value){
			this.busy = true
			this.selected_server_settings.jacktrip_q = q_value
			let requestObj = jsonrpc.request('1', 'set_q', {host: host, q_value: q_value})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_set_q(response)))
		},
		set_fpp(host, fpp_value){
			this.busy = true
			this.selected_server_settings.jack_fpp = fpp_value
			let requestObj = jsonrpc.request('1', 'set_fpp', {host: host, fpp_value: fpp_value})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_set_fpp(response)))
		},
		get_fpp(host){
			console.log(host)
			let requestObj = jsonrpc.request('1', 'get_fpp', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_get_fpp(response)))
		},
		get_q(host){
			let requestObj = jsonrpc.request('1', 'get_q', {host: host})
			return axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_get_q(response)))
		},
		restart_jacktrip(host){
			let requestObj = jsonrpc.request('1', 'restart_jacktrip', {host: host})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_restart_jacktrip(response)))
		},
		restart_jackd(host){
			let requestObj = jsonrpc.request('1', 'restart_jackd', {host: host})
			axios
				.post('/dashboard/rpc/', requestObj)
				.then(response => (this.handle_restart_jackd(response)))
		},
		handle_create_server(response){
			console.log(response)
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				// Return an error here instead and log in catch()
				this.busy = true
				// Deal with this at the end of the promise chain
				return response
			}
			this.ip = response.data.result.ip
			this.busy = false
			return response
		},
		handle_get_server_ip(response){
			console.log(response)
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				// Return an error here instead and log in catch()
				this.busy = true
				// Deal with this at the end of the promise chain
				return response
			}
			this.ip = response.data.result.ip
			this.busy = false
			console.log(response)
			return response
		},
		handle_get_fpp(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				// Return an error here instead and log in catch()
				this.busy = true
				// Deal with this at the end of the promise chain
				return response
			}
			this.selected_server_settings.jack_fpp = response.data.result.value
			this.server_settings.jack_fpp = response.data.result.value
			return response
		},
		handle_get_q(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				// Return an error here instead and log in catch()
				this.busy = true
				// Deal with this at the end of the promise chain
				return response
			}
			this.selected_server_settings.jacktrip_q = response.data.result.value
			this.server_settings.jacktrip_q = response.data.result.value
			return response
		},
		handle_set_q(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				// Return an error here instead and log in catch()
				this.busy = true
				// Deal with this at the end of the promise chain
				return
			}
			this.restart_jacktrip(this.ip)
		},
		handle_set_fpp(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				// Return an error here instead and log in catch()
				this.busy = true
				// Deal with this at the end of the promise chain
				return
			}
			this.restart_jackd(this.ip)
		},
		handle_restart_jacktrip(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				// Return an error here instead and log in catch()
				this.busy = true
				// Deal with this at the end of the promise chain
				return
			}
			this.get_q(this.ip)
			this.busy = false
		},
		handle_restart_jackd(response){
			if (response.data.error){
				window.alert(`An error occured:\n${response.data.error.message}`);
				// Return an error here instead and log in catch()
				this.busy = true
				// Deal with this at the end of the promise chain
				return
			}
			this.get_fpp(this.ip)
			this.busy = false
		},
	},
  mounted () {
		this.get_server_ip()
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
