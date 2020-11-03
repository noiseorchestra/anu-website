module.exports = {
    publicPath: process.env.NODE_ENV === 'production' ? 'https://sandreae-storage.fra1.digitaloceanspaces.com/anu-website/dist/' : 'http://127.0.0.1:8080',
    outputDir: '../server/static/dist',

    pages: {
      pages: {
        entry: "src/apps/pages/main.js", // matching the new paths created above
        template: "public/index.html",
        filename: '../../templates/vue/_vue_base.html', // relative to outputDir!
        chunks: ["chunk-vendors", "pages"],
      },
    //   dashboard: {
    //     entry: "./src/pages/dashboard/main.js", // matching the new paths created above
    //     template: "public/index.html",
    //     filename: '../../dashboard/templates/base-vue-dashboard.html', // relative to outputDir!
    //     chunks: ["chunk-vendors", "dashboard"],
    //   },
    },

    chainWebpack: config => {
        /*
        The arrow function in writeToDisk(...) tells the dev server to write
        only index.html to the disk.

        The indexPath option (see above) instructs Webpack to also rename
        index.html to base-vue.html and save it to Django templates folder.

        We don't need other assets on the disk (CSS, JS...) - the dev server
        can serve them from memory.

        See also:
        https://cli.vuejs.org/config/#indexpath
        https://webpack.js.org/configuration/dev-server/#devserverwritetodisk-
        */
        config.devServer
            .public('http://127.0.0.1:8080')
            .hotOnly(true)
            .headers({"Access-Control-Allow-Origin": "*"})
            .writeToDisk(filePath => filePath.endsWith('.html'));
    }
}
