<template>
  <div class="wrapper">
    <P5jsBackground></P5jsBackground>

    <div class="container">
      <nav class="desktop-nav nav" aria-label="desktop-nav-bar"><NavBar :routes="routes"></NavBar></nav>
      <nav class="mobile-nav nav" aria-label="mobile-nav-bar"><NavBarMobile :routes="routes"></NavBarMobile></nav>
      <div class="main">
        <div class="main__padding"></div>
        <router-view class="main__content"></router-view>
        <div class="main__padding"></div>
      </div>
      <footer class="footer"><Footer></Footer></footer>
    </div>
  </div>
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
    this.$router.push(`/${this.djangoData.slug}`).catch(err => {
      if (err.name !== 'NavigationDuplicated') {
        throw err;
      }
    });
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

.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  max-height: 100vh;
}

.nav {
  flex: 1 18px;;
}

.main {
  display: flex;
  flex-direction: row;
  justify-content: center;
  flex: 2 90vh;
  overflow-y: scroll;
}

.footer {
  flex: 1;
}

.main__content {
  flex: 3;
}

.main__padding {
  flex: 0;
}

@media (min-width: map-get($breakpoints, "medium")) {
  .main__padding {
    flex: 1;
  }
}

.mobile-nav {
	display: inline;
  max-height: 0px;
}

.desktop-nav {
  padding-bottom: 8px;
}

</style>
