import { mount, createLocalVue } from '@vue/test-utils';
import { axe, toHaveNoViolations } from 'jest-axe';
import App from '../App.vue';

expect.extend(toHaveNoViolations);

it('tests dashboard app with axe', async () => {
  const wrapper = mount(App);

  // test with axe
  const results = await axe(wrapper.element);

  expect(results).toHaveNoViolations();
});
