<template>
  <main id="app">
    <NavBar :routes="routes"></NavBar>
    <router-view></router-view>
    <P5jsBackground></P5jsBackground>
    <Footer></Footer>
  </main>
</template>

<script>
// @ is an alias to /src
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import P5jsBackground from '@/components/P5jsBackground.vue'
import PageContent from '../../views/page.vue'
import Home from '@/components/Home.vue'
import P5 from 'p5'

export default {
  name: 'App',
  data: function() {
    return {pages: {}}
  },
  components: {
    NavBar,
    P5jsBackground,
    Footer,
    Home
  },
  computed: {
    routes() {
      return this.$router.options.routes;
    },
  },
  methods: {
    generate_route: function (routeProps, component) {
      let new_route = {
        path: `/${routeProps.slug}`,
        name: routeProps.title,
        component: component,
        props: {routeProps: routeProps}
      }
      this.$router.options.routes.push(new_route)
      this.$router.addRoutes([new_route])
    },
    generate_page_routes: function (pages) {
      for (const page of pages) {
        if (page.slug === "home") {
          this.generate_route(page, Home)
          continue
        }
        this.generate_route(page, PageContent)
      }
    },
  },
  created: function () {
    // build routes and pass in djangoData
    let jsVariable = {
      slug: "about",
      pages: [{
        slug: "about",
        title: "About",
        body: "About stuff",
        nav_position: "02"
      }]
    }
    if (document.getElementById('djangoData')) {
      jsVariable = JSON.parse(document.getElementById('djangoData').textContent)
    }
    this.generate_page_routes(jsVariable.pages)
    this.pages = jsVariable.pages
    // this.$router.push(`/${jsVariable.slug}`).catch(err => {
    //   if (err.name !== 'NavigationDuplicated') {
    //     throw err;
    //   }
    // });
  }
}

</script>

<style>

#app {
  background-color: black;
  position: absolute;
  width: 100vw;
  left:0px;
  top: 0px;
  padding: 0px;
}

img {
  max-width: 100%;
}

</style>
