import Vue from 'vue';
import App from './App.vue';
import router from '../../router';

Vue.config.productionTip = false;

if (process.env.NODE_ENV === 'development') {
  const VueAxe = require('vue-axe').default;
  Vue.use(VueAxe);
}

new Vue({
  router,
  render: function (h) {
    return h(App);
  },
}).$mount('#app');
