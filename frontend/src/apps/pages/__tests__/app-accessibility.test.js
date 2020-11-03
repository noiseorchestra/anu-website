import { mount, createLocalVue } from '@vue/test-utils'
import {axe, toHaveNoViolations} from 'jest-axe'
import VueRouter from 'vue-router'
import App from '../App.vue'

expect.extend(toHaveNoViolations)

it('test pages app with axe', async () => {

	// create router with dummy routes
	const localVue = createLocalVue()
	localVue.use(VueRouter)
	const routes = [
		{
	    path: '/dummy',
	    name: 'Dummy'
		}
	]
	const router = new VueRouter({
    routes
	})
	// router.push({name: 'About', params: {}})

	//mount the app
	const wrapper = mount(App, {
	  localVue,
	  router,
	})

	//test with axe
  const results = await axe(wrapper.element)

  expect(results).toHaveNoViolations()
})
