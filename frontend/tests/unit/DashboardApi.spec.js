import { mount } from "@vue/test-utils";
import DashboardApi from "@/components/DashboardApi.vue";
import axios from "axios";
import jsonrpc from "jsonrpc-lite";

jest.mock("axios");

describe("onStartRPC method in DashboardApi.vue", () => {
  it("should increment rpcCount data attribute", () => {
    const wrapper = mount(DashboardApi);

    expect(wrapper.vm.rpcCount).toBe(0);
    wrapper.vm.onStartRPC();
    expect(wrapper.vm.rpcCount).toBe(1);
  });
});

describe("onFinishRPC method in DashboardApi.vue", () => {
  it("should decrese rpcCount data attribute", () => {
    const wrapper = mount(DashboardApi, {
      data() {
        return { rpcCount: 1 };
      },
    });

    expect(wrapper.vm.rpcCount).toBe(1);
    wrapper.vm.onFinishRPC();
    expect(wrapper.vm.rpcCount).toBe(0);
  });
});

describe("toggle deactivate class in DashboardApi.vue", () => {
  it("should toggle component if more than 0 RPC in progress", async () => {
    const wrapper = mount(DashboardApi, {
      data() {
        return { rpcCount: 0 };
      },
    });

    expect(wrapper.find(".api-container").classes()).not.toContain(
      "deactivate"
    );
    wrapper.vm.onStartRPC();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.serverCallInProgress).toBe(true);
    expect(wrapper.find(".api-container").classes()).toContain("deactivate");
    wrapper.vm.onFinishRPC();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.serverCallInProgress).toBe(false);
    expect(wrapper.find(".api-container").classes()).not.toContain(
      "deactivate"
    );
  });
});

describe("checkForError method in DashboardApi.vue", () => {
  it("throws an error if the RPC failed", () => {
    const wrapper = mount(DashboardApi);

    let mockResponse = {
      data: {
        error: {
          message: "Error",
        },
      },
    };

    expect(() => {
      wrapper.vm.checkForError(mockResponse);
    }).toThrow(new Error("Error"));
  });
});

describe("executeRPC method in DashboardApi.vue", () => {
  it("Should execute an RPC based on requestObj", () => {
    const wrapper = mount(DashboardApi);

    let requestObj = jsonrpc.request("1", "fetch_all_servers", {
      host: "234.234.234.234",
    });
    const ip = "123.123.123.123";
    const resp = {
      data: {
        result: "123.123.123.123",
      },
    };

    axios.post.mockResolvedValue(resp);

    return wrapper.vm.executeRPC(requestObj).then((data) => {
      expect(data).toEqual(ip);
      expect(wrapper.vm.rpcCount).toEqual(0);
    });
  });
});

describe("fetchServerDetails async method in DashboardApi.vue", () => {
  it("should fetch fpp and q from server and update component", () => {
    const wrapper = mount(DashboardApi);

    const ip = "123.123.123.123";
    const resp1 = {
      data: {
        result: "256",
      },
    };
    const resp2 = {
      data: {
        result: "6",
      },
    };

    axios.post.mockResolvedValueOnce(resp1);
    axios.post.mockResolvedValueOnce(resp2);

    return wrapper.vm.fetchServerDetails(ip).then((data) => {
      expect(wrapper.vm.q).toEqual("6");
      expect(wrapper.vm.fpp).toEqual("256");
    });
  });
});

describe("waitForReady async method in DashboardApi.vue", () => {
  it("should block until server status is 'running'", async () => {
    const ip = "123.123.123.123";
    const resp1 = "provisioning";
    const resp2 = "booting";
    const resp3 = "running";

    const wrapper = mount(DashboardApi);

    wrapper.vm.getServerStatus = jest.fn();

    wrapper.vm.getServerStatus.mockResolvedValueOnce(resp1);
    wrapper.vm.getServerStatus.mockResolvedValueOnce(resp2);
    wrapper.vm.getServerStatus.mockResolvedValueOnce(resp3);

    let data = await wrapper.vm.waitForReady(ip, 50, 10);
    expect(data).toEqual("running");
  });
});

describe("waitForReady async method in DashboardApi.vue", () => {
  it("should throw an error if waiting too long", () => {
    const ip = "123.123.123.123";
    const wrapper = mount(DashboardApi);

    wrapper.vm.getServerStatus = jest.fn();
    wrapper.vm.getServerStatus.mockResolvedValue("booting");

    return wrapper.vm
      .waitForReady(ip, 50, 10)
      .catch((e) =>
        expect(e).toEqual(
          new Error("Timeout, waited too long for server to boot.")
        )
      );
  });
});
