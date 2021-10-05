<template>
  <div :class="{ deactivate: disabled }" class="api-container">
    <div class="current-info">
      <div><h2>JackTrip Hub Server Settings</h2></div>
      <div class="api-container-child jacktrip-queue">
        <div class="key">JackTrip queue:</div>
        <div class="values">
          <div
            v-for="value in qValues"
            :key="value"
            :class="{ deactivate: !q }"
          >
            <button
              class="api-button"
              :class="{ selected: q == value }"
              @click="changePyPatcherQ(ip, value)"
            >
              {{ value }}
            </button>
          </div>
        </div>
      </div>
      <div class="api-container-child jack-fpp">
        <div class="key">JACK fpp:</div>
        <div class="values">
          <div
            v-for="value in fppValues"
            :key="value"
            :class="{ deactivate: !fpp }"
          >
            <button
              class="api-button"
              :class="{ selected: fpp == value }"
              @click="changePyPatcherFpp(ip, value)"
            >
              {{ value }}
            </button>
          </div>
        </div>
      </div>
      <div class="api-container-child server-details">
        <div class="key">Server IP:</div>
        <div class="values">
          <div v-if="ip">
            {{ ip }}
          </div>
          <div>
            <button class="api-button" @click="refreshDetails()">
              refresh
            </button>
          </div>
        </div>
      </div>
      <div class="api-container-child server-details">
        <div class="key">status:</div>
        <div class="values">
          <div>{{ serverStatus }}</div>
        </div>
      </div>
      <div class="api-container-child server-automation">
        <div class="key" />
        <div class="values">
          <div>
            <button
              v-if="!ip"
              class="api-button"
              @click="initServer()"
            >
              new server
            </button>
            <button v-else class="api-button" @click="deleteServer()">
              delete server
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../assets/js/dashboardApi.js';

export default {
  name: 'DashboardApi',
  data() {
    return {
      rpcCount: 0,
      serverStatus: 'checking server...',
      ip: null,
      q: null,
      fpp: null,
      qValues: [4, 6, 8, 10, 12, 14, 16],
      fppValues: [64, 128, 256, 512],
    };
  },
  computed: {
    // a computed getter
    disabled: function () {
      // `this` points to the vm instance
      return this.rpcCount != 0;
    },
  },
  mounted() {
    this.refreshDetails();
  },
  methods: {
    async initServer() {
      this.onStartRPC();
      // create the server
      try {
        const host = await api.createServer();
        // wait for server to boot
        await this.waitForReady(host);
        this.serverStatus =
          'Installing dependencies (will take approx. 10mins)';
        // extra wait to be safe
        await new Promise((r) => setTimeout(r, 120000));
        await api.uploadScripts(host);
        // extra wait while rebooting
        this.serverStatus = 'Installation complete, rebooting server';
        await new Promise((r) => setTimeout(r, 240000));
      } catch (error) {
        this.serverStatus = error.message;
      } finally {
        this.refreshDetails();
        this.onFinishRPC();
      }
    },
    async refreshDetails() {
      try {
        this.onStartRPC();
        this.ip = null;
        this.fpp = null;
        this.q = null;
        this.ip = await api.getServerIP();
        const { ip, fpp, q, serverStatus } =
          await api.fetchServerDetails();
        this.fpp = fpp;
        this.q = q;
        this.serverStatus = serverStatus;
      } catch (error) {
        this.serverStatus = error.message;
      } finally {
        this.onFinishRPC();
      }
    },
    async waitForReady(host, interval = 5000, attempts = 20) {
      let response;
      let count = 0;
      while (response !== 'running') {
        count++;
        response = await api.getServerStatus(host);
        this.serverStatus = response;
        if (count == attempts) {
          throw new Error(
            'Timeout, waited too long for server to boot.',
          );
        }
        await new Promise((r) => setTimeout(r, interval));
      }
      return response;
    },
    async changePyPatcherFpp(host, value) {
      this.onStartRPC();
      try {
        await api.changePyPatcherFpp(host, value);
      } catch (error) {
        this.serverStatus = error.message;
      } finally {
        this.refreshDetails();
        this.onFinishRPC();
      }
    },
    async changePyPatcherQ(host, value) {
      this.onStartRPC();
      try {
        await api.changePyPatcherQ(host, value);
      } catch (error) {
        this.serverStatus = error.message;
      } finally {
        this.refreshDetails();
        this.onFinishRPC();
      }
    },
    async deleteServer() {
      this.onStartRPC();
      try {
        await api.deleteServer();
        this.ip = null;
        this.fpp = null;
        this.q = null;
        this.serverStatus = 'Server deleted';
      } catch (error) {
        this.serverStatus = error.message;
      } finally {
        this.onFinishRPC();
      }
    },
    onStartRPC() {
      this.rpcCount += 1;
    },
    onFinishRPC() {
      this.rpcCount -= 1;
    },
  },
};
</script>

<style scoped lang="scss">
@import '@/scss/_variables.scss';
@import '@/scss/_common.scss';
@include api-style;

.api-container {
  display: flex;
  flex-direction: column;
  color: map-get($colors, 'bright');
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
