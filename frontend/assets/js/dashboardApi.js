import jsonrpc from 'jsonrpc-lite';
import axios from 'axios';

const dashboardApi = {
  async fetchServerDetails() {
    try {
      const host = await dashboardApi.getServerIP();
      const fpp = await dashboardApi.getFpp(host);
      const q = await dashboardApi.getQ(host);
      return {
        ip: host,
        fpp: fpp,
        q: q,
        serverStatus: 'running',
      };
    } catch (error) {
      throw new Error(error.message);
    }
  },
  async changePyPatcherFpp(host, value) {
    try {
      await dashboardApi.setFpp(host, value);
      const response = await dashboardApi.restartJack(host);
      return response;
    } catch (error) {
      throw new Error(error.message);
    }
  },
  async changePyPatcherQ(host, value) {
    try {
      await dashboardApi.setQ(host, value);
      const response = await dashboardApi.restartJackTrip(host);
      return response;
    } catch (error) {
      throw new Error(error.message);
    }
  },
  createServer() {
    const requestObj = jsonrpc.request('1', 'create_server');
    return dashboardApi.executeRPC(requestObj);
  },
  setupServer(host) {
    const requestObj = jsonrpc.request('1', 'setup_server', {
      host: host,
    });
    return dashboardApi.executeRPC(requestObj);
  },
  installPypatcher() {
    const requestObj = jsonrpc.request('1', 'install_pypatcher');
    return dashboardApi.executeRPC(requestObj);
  },
  deleteServer() {
    const requestObj = jsonrpc.request('1', 'delete_all_servers');
    return dashboardApi.executeRPC(requestObj);
  },
  setQ(host, qValue) {
    const requestObj = jsonrpc.request('1', 'set_q', {
      host: host,
      q_value: qValue,
    });
    return dashboardApi.executeRPC(requestObj);
  },
  setFpp(host, fppValue) {
    const requestObj = jsonrpc.request('1', 'set_fpp', {
      host: host,
      fpp_value: fppValue,
    });
    return dashboardApi.executeRPC(requestObj);
  },
  getServerIP() {
    const requestObj = jsonrpc.request('1', 'fetch_all_servers');
    return dashboardApi.executeRPC(requestObj);
  },
  getServerStatus(host) {
    const requestObj = jsonrpc.request('1', 'get_server_status', {
      host: host,
    });
    return dashboardApi.executeRPC(requestObj);
  },
  getFpp(host) {
    const requestObj = jsonrpc.request('1', 'get_fpp', {
      host: host,
    });
    return dashboardApi.executeRPC(requestObj);
  },
  getQ(host) {
    const requestObj = jsonrpc.request('1', 'get_q', { host: host });
    return dashboardApi.executeRPC(requestObj);
  },
  restartJackTrip(host) {
    const requestObj = jsonrpc.request('1', 'restart_jacktrip', {
      host: host,
    });
    return dashboardApi.executeRPC(requestObj);
  },
  restartJack(host) {
    const requestObj = jsonrpc.request('1', 'restart_jackd', {
      host: host,
    });
    return dashboardApi.executeRPC(requestObj);
  },
  async executeRPC(requestObj) {
    return axios
      .post('/dashboard/rpc/', requestObj)
      .then((response) => dashboardApi.checkForError(response))
      .then((response) => {
        return response.data.result;
      })
      .catch((error) => dashboardApi.handleServerCallError(error));
  },
  checkForError(response) {
    if (response.data.error) {
      throw new Error(response.data.error.message);
    }
    return response;
  },
  handleServerCallError(error) {
    throw new Error(error.message);
  },
};

export default dashboardApi;
