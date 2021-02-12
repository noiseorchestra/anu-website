import jsonrpc from "jsonrpc-lite";
import axios from "axios";

const dashboardApi = {
  // async initServer () {
  //     try {
  //         let host = await createServer()
  //         // wait for server to boot
  //         await waitForReady(host)
  //         serverStatus = "installing dependencies (will take approx. 10mins)"
  //         // extra wait to be safe
  //         await new Promise(r => setTimeout(r, 60000));
  //         await uploadScripts(host)
  //         // extra wait while rebooting
  //         await new Promise(r => setTimeout(r, 120000));
  //         let response = await fetchServerDetails()
  //         return response
  //     } catch(error) {
  //         throw new Error(error.message)
  //     }
  // },
  async fetchServerDetails() {
    try {
      let host = await dashboardApi.getServerIP();
      let fpp = await dashboardApi.getFpp(host);
      let q = await dashboardApi.getQ(host);
      return {
        ip: host,
        fpp: fpp,
        q: q,
        serverStatus: "running",
      };
    } catch (error) {
      throw new Error(error.message);
    }
  },
  async changePyPatcherFpp(host, value) {
    try {
      await dashboardApi.setFpp(host, value);
      await dashboardApi.restartJack(host);
      let response = await dashboardApi.fetchServerDetails();
      return response;
    } catch (error) {
      return error.message;
    }
  },
  async changePyPatcherQ(host, value) {
    try {
      await dashboardApi.setQ(host, value);
      await dashboardApi.restartJackTrip(host);
      let response = await dashboardApi.fetchServerDetails();
      return response;
    } catch (error) {
      return error.message;
    }
  },
  createServer() {
    let requestObj = jsonrpc.request("1", "create_server");
    return dashboardApi.executeRPC(requestObj);
  },
  uploadScripts(host) {
    let requestObj = jsonrpc.request("1", "upload_scripts", { host: host });
    return dashboardApi.executeRPC(requestObj);
  },
  deleteServer() {
    let requestObj = jsonrpc.request("1", "delete_all_servers");
    return dashboardApi.executeRPC(requestObj);
  },
  setQ(host, q_value) {
    let requestObj = jsonrpc.request("1", "set_q", {
      host: host,
      q_value: q_value,
    });
    return dashboardApi.executeRPC(requestObj);
  },
  setFpp(host, fpp_value) {
    let requestObj = jsonrpc.request("1", "set_fpp", {
      host: host,
      fpp_value: fpp_value,
    });
    return dashboardApi.executeRPC(requestObj);
  },
  getServerIP() {
    let requestObj = jsonrpc.request("1", "fetch_all_servers");
    return dashboardApi.executeRPC(requestObj);
  },
  getServerStatus(host) {
    let requestObj = jsonrpc.request("1", "get_server_status", { host: host });
    return dashboardApi.executeRPC(requestObj);
  },
  getFpp(host) {
    let requestObj = jsonrpc.request("1", "get_fpp", { host: host });
    return dashboardApi.executeRPC(requestObj);
  },
  getQ(host) {
    let requestObj = jsonrpc.request("1", "get_q", { host: host });
    return dashboardApi.executeRPC(requestObj);
  },
  restartJackTrip(host) {
    let requestObj = jsonrpc.request("1", "restart_jacktrip", { host: host });
    return dashboardApi.executeRPC(requestObj);
  },
  restartJack(host) {
    let requestObj = jsonrpc.request("1", "restart_jackd", { host: host });
    return dashboardApi.executeRPC(requestObj);
  },
  executeRPC(requestObj) {
    return axios
      .post("/dashboard/rpc/", requestObj)
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
    console.log(error.message);
    throw new Error(error.message);
  },
  test(hello) {
    console.log(hello);
  },
};

export default dashboardApi;
