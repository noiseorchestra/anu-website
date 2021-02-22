module.exports = {
  preset: '@vue/cli-plugin-unit-jest/presets/no-babel',
  transformIgnorePatterns: ['/node_modules/'],
  transform: {
    '.*\\.(vue)$': 'vue-jest',
    '^.+\\.tsx?$': 'ts-jest',
  },
  moduleFileExtensions: [
    'js',
    'jsx',
    'json',
    'vue',
    'ts',
    'tsx',
    'node',
  ],
  setupFiles: ['jest-canvas-mock'],
};
