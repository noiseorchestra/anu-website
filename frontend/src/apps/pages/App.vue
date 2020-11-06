<template>
  <main id="app">
    <span class="desktopNav"><NavBar :routes="routes"></NavBar></span>
    <span class="mobileNav"><NavBarMobile :routes="routes"></NavBarMobile></span>
    <router-view></router-view>
    <P5jsBackground></P5jsBackground>
    <Footer></Footer>
  </main>
</template>

<script>
// @ is an alias to /src
import NavBar from '@/components/NavBar.vue'
import NavBarMobile from '@/components/NavBarMobile.vue'
import Footer from '@/components/Footer.vue'
import P5jsBackground from '@/components/P5jsBackground.vue'
import PageView from '../../views/page.vue'
import Home from '@/components/Home.vue'
import P5 from 'p5'

export default {
  name: 'App',
  // data: function() {
  //   return {pages: {}}
  // },
  data: function() {
    return {
      djangoData: {
        slug: "about",
        pages: [{
          slug: "about",
          title: "About",
          body: "About stuff",
          nav_position: "02"
        }]
      }
    }
  },
  components: {
    NavBar,
    NavBarMobile,
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
    generate_page_routes: function () {
      for (const page of this.djangoData.pages) {
        if (page.slug === "home") {
          this.generate_route(page, Home)
          continue
        }
        this.generate_route(page, PageView)
      }
    },
  },
  created: function () {
    // build routes and pass in djangoData
    if (document.getElementById('djangoData')) {
      this.djangoData = JSON.parse(document.getElementById('djangoData').textContent)
    }
    this.generate_page_routes()
    // this.pages = jsVariable.pages
    // this.$router.push(`/${jsVariable.slug}`).catch(err => {
    //   if (err.name !== 'NavigationDuplicated') {
    //     throw err;
    //   }
    // });
  }
}

</script>

<style lang="scss">
@import "@/scss/_common.scss";
@include base-style;
@include link-style;
@include nav-style;
</style>

<style scoped lang="scss">
@import "@/scss/_variables.scss";

.mobileNav {
  display: none;
}
.desktopNav {
  display: block;
}

@media (max-width: map-get($breakpoints, "small")) {
  .mobileNav {
    display: block;
  }
  .desktopNav {
    display: none;
  }
}

</style>
