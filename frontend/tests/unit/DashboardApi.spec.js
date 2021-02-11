import { mount } from '@vue/test-utils'
import DashboardApi from '@/components/DashboardApi.vue'

describe('DashboardApi.vue', () => {
  it('renders a greeting', () => {
    const wrapper = mount(DashboardApi)

    console.log(wrapper.html())
  })
})
