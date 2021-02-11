import { mount } from '@vue/test-utils'
import DashboardApi from '@/components/DashboardApi.vue'
import axios from 'axios';
import jsonrpc from 'jsonrpc-lite'

jest.mock('axios');


describe('checkForError method in DashboardApi.vue', () => {
  it('throws an error if the RPC failed', () => {
    const wrapper = mount(DashboardApi)

    let mockResponse = {
        data: {
            error: {
                message: "Error"
            }
        }
    }
    
    expect(() => {
        wrapper.vm.checkForError(mockResponse);
    }).toThrow(new Error('Error'));
  })
})

describe('executeRPC method in DashboardApi.vue', () => {
  it('Should execute an RPC based on requestObj', () => {
    const wrapper = mount(DashboardApi)

    let requestObj = jsonrpc.request('1', 'fetch_all_servers', {host: "234.234.234.234"})
    const ip = '123.123.123.123'
    const resp = {
        data: {
            result: {
                value: "123.123.123.123"
            }
        }}
    
    axios.post.mockResolvedValue(resp);
  
    return wrapper.vm.executeRPC(requestObj).then(data => {
        expect(data).toEqual(ip)});
  })
})
