module.exports = {
    extends: [
        // add more generic rulesets here, such as:
        // 'eslint:recommended',
        //   'plugin:vue/vue3-recommended',
        'plugin:vue/recommended', // Use this if you are using Vue.js 2.x.
        'plugin:prettier/recommended'
    ],
    rules: {
        // override/add rules settings here, such as:
        //   'vue/no-unused-vars': 'error'
        "global-require": 0,
        "vue/no-use-v-if-with-v-for": "off"
    }
  }