<template>
  <div class="wrapper">
    <P5jsBackground></P5jsBackground>

    <div class="container">
      <NavBarWrapper :pages="data.pages" />
      <main class="main">
        <div class="main__padding"></div>
        <router-view class="main__content"></router-view>
        <div class="main__padding"></div>
      </main>
      <footer class="footer"><Footer /></footer>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import NavBarWrapper from '@/components/NavBarWrapper.vue';
import Footer from '@/components/Footer.vue';
import P5jsBackground from '@/components/P5jsBackground.vue';
import PageView from '../../views/page.vue';
import Home from '@/components/Home.vue';
import Listen from '@/components/Listen.vue';

export default {
  name: 'App',
  data: function () {
    return {
      data: {
        slug: '',
        pages: [],
      },
    };
  },
  components: {
    NavBarWrapper,
    P5jsBackground,
    Footer,
  },
  methods: {
    generate_route: function (page, component) {
      const newRoute = {
        path: `/${page.slug}`,
        name: page.title,
        component: component,
        props: { page: page },
      };
      this.$router.options.routes.push(newRoute);
      this.$router.addRoutes([newRoute]);
    },
    generate_page_routes: function () {
      for (const page of this.data.pages) {
        if (page.slug === 'home') {
          this.generate_route(page, Home);
          continue;
        }
        if (page.slug === 'listen') {
          this.generate_route(page, Listen);
          continue;
        }
        this.generate_route(page, PageView);
      }
    },
  },
  created: function () {
    // build routes and pass in data
    if (document.getElementById('djangoData')) {
      this.data = JSON.parse(
        document.getElementById('djangoData').textContent,
      );
    }
    this.generate_page_routes();
    this.$router.push(`/${this.data.slug}`).catch((err) => {
      if (err.name !== 'NavigationDuplicated') {
        throw err;
      }
    });
  },
};
</script>

<style lang="scss">
@font-face {
  font-family: 'Russian';
  src: url('../../../assets/fonts/Russian.woff') format('woff'),
    url('../../../assets/fonts/Russian.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: block;
}
@import '@/scss/_common.scss';
@include base-style;
@include link-style;
@include nav-style;
</style>

<style scoped lang="scss">
@import '@/scss/_variables.scss';

.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  max-height: 100vh;
}

.main {
  display: flex;
  flex-direction: row;
  justify-content: center;
  flex: 1 1 100%;
  overflow-y: scroll;
  margin-top: 0px;
  margin-bottom: 0px;
}

.main__content {
  flex: 3;
}

.main__padding {
  flex: 0;
}

.footer {
  height: 20px;
  display: block;
  position: fixed;
  bottom: 0px;
  padding-bottom: 3px;
  width: 100%;
}

@media (min-width: map-get($breakpoints, 'medium')) {
  .main__padding {
    flex: 1;
  }
  .nav {
    height: 20px;
  }
}
</style>
