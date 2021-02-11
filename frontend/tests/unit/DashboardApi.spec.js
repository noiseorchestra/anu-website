import { mount } from "@vue/test-utils";
import DashboardApi from "@/components/DashboardApi.vue";
import axios from "axios";
import jsonrpc from "jsonrpc-lite";

jest.mock("axios");

describe("onStartRPC method in DashboardApi.vue", () => {
  it("should increment rpc_count data attribute", () => {
    const wrapper = mount(DashboardApi);

    expect(wrapper.vm.rpc_count).toBe(0);
    wrapper.vm.onStartRPC();
    expect(wrapper.vm.rpc_count).toBe(1);
  });
});

describe("onFinishRPC method in DashboardApi.vue", () => {
  it("should decrese rpc_count data attribute", () => {
    const wrapper = mount(DashboardApi, {
      data() {
        return { rpc_count: 1 };
      },
    });

    expect(wrapper.vm.rpc_count).toBe(1);
    wrapper.vm.onFinishRPC();
    expect(wrapper.vm.rpc_count).toBe(0);
  });
});

describe("toggle deactivate class in DashboardApi.vue", () => {
  it("should toggle component if more than 0 RPC in progress", async () => {
    const wrapper = mount(DashboardApi, {
      data() {
        return { rpc_count: 0 };
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
        result: "123.123.123.123"
      },
    };

    axios.post.mockResolvedValue(resp);

    return wrapper.vm.executeRPC(requestObj).then((data) => {
      expect(data).toEqual(ip);
      expect(wrapper.vm.rpc_count).toEqual(0);
    });
  });
});

describe("fetchServerDetails async method in DashboardApi.vue", () => {
  it("should fetch fpp and q from server and update component", () => {
    const wrapper = mount(DashboardApi);
 
    const ip = "123.123.123.123";
    const resp1 = {
      data: {
        result: "256"
      },
    };
    const resp2 = {
      data: {
        result: "6"
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
