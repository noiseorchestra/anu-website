import { mount } from '@vue/test-utils';
import DashboardApi from '@/components/DashboardApi.vue';
import axios from 'axios';
import jsonrpc from 'jsonrpc-lite';
import api from '../../assets/js/dashboardApi.js';

jest.mock('axios');

const mockResponseSuccess = (payload) => {
  return {
    data: {
      result: payload,
    },
  };
};
let mockResponseError = {
  data: {
    error: {
      message: 'Error',
    },
  },
};

describe('fetchServerDetails from dashboardApi', () => {
  it('should return server details on success or throw error', async () => {
    axios.post.mockResolvedValueOnce(
      mockResponseSuccess('123.123.123.123'),
    );
    axios.post.mockResolvedValueOnce(mockResponseSuccess('256'));
    axios.post.mockResolvedValueOnce(mockResponseSuccess('8'));

    let response = await api.fetchServerDetails();
    expect(response).toStrictEqual({
      ip: '123.123.123.123',
      fpp: '256',
      q: '8',
      serverStatus: 'running',
    });

    axios.post.mockResolvedValueOnce(mockResponseError);
    await expect(api.fetchServerDetails()).rejects.toThrow(
      new Error('Error'),
    );
  });
});

describe('changePyPatcherFpp from dashboardApi', () => {
  it('should return server details on success or throw error', async () => {
    axios.post.mockResolvedValueOnce(mockResponseSuccess('0'));
    axios.post.mockResolvedValueOnce(mockResponseSuccess('0'));

    let response = await api.changePyPatcherFpp(
      '123.123.123.123',
      '256',
    );
    expect(response).toStrictEqual('0');

    axios.post.mockResolvedValueOnce(mockResponseError);
    await expect(api.changePyPatcherFpp()).rejects.toThrow(
      new Error('Error'),
    );
  });
});

describe('changePyPatcherQ from dashboardApi', () => {
  it('should return server details on success or throw error', async () => {
    axios.post.mockResolvedValueOnce(mockResponseSuccess('0'));
    axios.post.mockResolvedValueOnce(mockResponseSuccess('0'));

    let response = await api.changePyPatcherQ('123.123.123.123', '8');
    expect(response).toStrictEqual('0');

    axios.post.mockResolvedValueOnce(mockResponseError);
    await expect(api.changePyPatcherQ()).rejects.toThrow(
      new Error('Error'),
    );
  });
});

describe('executeRPC method in dashboardApi', () => {
  it('Should execute an RPC based on requestObj or throw error', async () => {
    let requestObj = jsonrpc.request('1', 'fetch_all_servers', {
      host: '234.234.234.234',
    });

    const ip = '123.123.123.123';

    axios.post.mockResolvedValue(mockResponseSuccess(ip));

    let response = await api.executeRPC(requestObj);
    expect(response).toEqual(ip);

    axios.post.mockResolvedValueOnce(mockResponseError);
    await expect(api.executeRPC()).rejects.toThrow(
      new Error('Error'),
    );
  });
});

describe('checkForError method in dashboardApi', () => {
  it('Should throw error if RPC response contains error message', async () => {
    let mockResponse = mockResponseSuccess('0');
    let response = api.checkForError(mockResponse);
    expect(response).toEqual(mockResponse);

    expect(() => {
      api.checkForError(mockResponseError);
    }).toThrow(new Error('Error'));
  });
});

describe('onStartRPC method in DashboardApi.vue', () => {
  it('should increment rpcCount data attribute', async () => {
    axios.post.mockResolvedValueOnce(
      mockResponseSuccess('123.123.123.123'),
    );
    axios.post.mockResolvedValueOnce(mockResponseSuccess('256'));
    axios.post.mockResolvedValueOnce(mockResponseSuccess('6'));

    let wrapper = mount(DashboardApi);
    // wait for component to mount
    await new Promise((r) => setTimeout(r, 500));
    expect(wrapper.vm.rpcCount).toBe(0);
    wrapper.vm.onStartRPC();
    expect(wrapper.vm.rpcCount).toBe(1);
    wrapper.vm.onFinishRPC();
    expect(wrapper.vm.rpcCount).toBe(0);
  });
});

describe('toggle deactivate class in DashboardApi.vue', () => {
  it('should toggle component if more than 0 RPC in progress', async () => {
    axios.post.mockResolvedValueOnce(
      mockResponseSuccess('123.123.123.123'),
    );
    axios.post.mockResolvedValueOnce(mockResponseSuccess('256'));
    axios.post.mockResolvedValueOnce(mockResponseSuccess('6'));

    let wrapper = mount(DashboardApi);
    // wait for component to mount
    await new Promise((r) => setTimeout(r, 500));
    expect(wrapper.find('.api-container').classes()).not.toContain(
      'deactivate',
    );
    wrapper.vm.onStartRPC();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.disabled).toBe(true);
    expect(wrapper.find('.api-container').classes()).toContain(
      'deactivate',
    );
    wrapper.vm.onFinishRPC();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.disabled).toBe(false);
    expect(wrapper.find('.api-container').classes()).not.toContain(
      'deactivate',
    );
  });
});

describe('waitForReady async method in DashboardApi.vue', () => {
  it('should throw an error if waiting too long', async () => {
    const ip = '123.123.123.123';
    const wrapper = mount(DashboardApi);

    api.getServerStatus = jest.fn();
    api.getServerStatus.mockResolvedValue('booting');

    await expect(wrapper.vm.waitForReady(ip, 50, 10)).rejects.toThrow(
      new Error('Timeout, waited too long for server to boot.'),
    );
    expect(api.getServerStatus).toHaveBeenCalledTimes(10);
  });
});

describe('waitForReady async method in DashboardApi.vue', () => {
  it('should throw an error if waiting too long', async () => {
    const ip = '123.123.123.123';
    const wrapper = mount(DashboardApi);

    api.getServerStatus = jest.fn();
    api.getServerStatus.mockResolvedValueOnce('provisioning');
    api.getServerStatus.mockResolvedValueOnce('booting');
    api.getServerStatus.mockResolvedValueOnce('running');

    let response = await wrapper.vm.waitForReady(ip, 50, 10);
    expect(response).toBe('running');
    expect(api.getServerStatus).toHaveBeenCalledTimes(3);
  });
});
