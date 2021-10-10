module.exports = {
  publicPath:
    process.env.NODE_ENV === 'production'
      ? 'https://sandreae-storage.fra1.digitaloceanspaces.com/anu-website/dist/'
      : 'http://127.0.0.1:8080',
  outputDir: 'build/dist',
  pages: {
    pages: {
      entry: 'src/apps/pages/main.js',
      template: 'public/index.html',
      filename: '../templates/pages.html', // relative to outputDir!
      chunks: ['chunk-vendors', 'pages'],
    },
    dashboard: {
      entry: 'src/apps/dashboard/main.js',
      template: 'public/index.html',
      filename: '../templates/dashboard.html', // relative to outputDir!
      chunks: ['chunk-vendors', 'dashboard'],
    },
  },
  chainWebpack: (config) => {
    config.devServer
      .public('http://127.0.0.1:8080')
      .hotOnly(true)
      .headers({ 'Access-Control-Allow-Origin': '*' })
      .writeToDisk((filePath) => filePath.endsWith('.html'));
  },
};
