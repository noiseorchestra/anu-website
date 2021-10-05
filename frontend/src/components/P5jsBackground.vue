<template>
  <div id="canvas" />
</template>

<script>
import P5 from 'p5';

export default {
  name: 'P5jsBackground',
  data: function () {
    return { sketch: null };
  },
  created: function () {
    const sketch = (s) => {
      const fr = 1;

      let ORANGE;
      let SHUKOV;
      let METRO;
      let CACTUS;
      let CAM;
      let COSMOS;
      let CRYS;
      let MILL;
      let MOSCOW;
      let LIGHT;
      let HIRO;
      let TABLET;
      let STONE;

      s.preload = () => {
        SHUKOV = s.loadImage(require('../../assets/SHUKOV.png'));
        METRO = s.loadImage(require('../../assets/METRO.png'));
        ORANGE = s.loadImage(require('../../assets/ORANGE.png'));
        CACTUS = s.loadImage(require('../../assets/CACTUS.png'));
        CAM = s.loadImage(require('../../assets/CAM.png'));
        COSMOS = s.loadImage(require('../../assets/COSMOS.png'));
        CRYS = s.loadImage(require('../../assets/CRYS.png'));
        MILL = s.loadImage(require('../../assets/MILL.png'));
        MOSCOW = s.loadImage(require('../../assets/MOSCOW.png'));
        LIGHT = s.loadImage(require('../../assets/LIGHT.png'));
        HIRO = s.loadImage(require('../../assets/HIRO.png'));
        TABLET = s.loadImage(require('../../assets/TABLET.png'));
        STONE = s.loadImage(require('../../assets/STONE.png'));
      };

      s.setup = () => {
        s.createCanvas(window.innerWidth, window.innerHeight + 100);
        s.frameRate(fr);
      };

      s.draw = () => {
        const width = window.innerWidth + 200;
        const height = window.innerHeight + 200;
        s.clear();
        s.background(220, 10);
        s.image(
          SHUKOV,
          s.random(width) - 200,
          s.random(height) - 200,
          180,
          180,
        );
        s.image(
          METRO,
          s.random(width) - 200,
          s.random(height) - 200,
          200,
          180,
        );
        s.image(
          ORANGE,
          s.random(width) - 200,
          s.random(height) - 200,
          150,
          150,
        );
        s.image(
          CACTUS,
          s.random(width) - 200,
          s.random(height) - 200,
          200,
          200,
        );
        s.image(
          CAM,
          s.random(width) - 200,
          s.random(height) - 200,
          200,
          200,
        );
        s.image(
          COSMOS,
          s.random(width) - 200,
          s.random(height) - 200,
          200,
          200,
        );
        s.image(
          CRYS,
          s.random(width) - 200,
          s.random(height) - 200,
          200,
          200,
        );
        s.image(
          MILL,
          s.random(width) - 200,
          s.random(height) - 200,
          200,
          200,
        );
        s.image(
          MOSCOW,
          s.random(width) - 200,
          s.random(height) - 200,
          200,
          200,
        );
        s.image(
          LIGHT,
          s.random(width) - 200,
          s.random(height) - 200,
          200,
          200,
        );
        s.image(
          HIRO,
          s.random(width) - 200,
          s.random(height) - 200,
          300,
          285,
        );
        s.image(
          TABLET,
          s.random(width) - 200,
          s.random(height) - 200,
          200,
          200,
        );
        s.image(
          STONE,
          s.random(width) - 200,
          s.random(height) - 200,
          170,
          230,
        );
      };
      this.sketch = s;
    };
    // eslint-disable-next-line no-unused-vars
    const canvas = new P5(sketch, 'canvas');
  },
  mounted() {
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize: function () {
      // Calculate new canvas size based on window
      this.$nextTick(() => {
        this.sketch.resizeCanvas(
          window.innerWidth,
          window.innerHeight,
        );
      });
    },
  },
};
</script>

<style scoped>
#canvas {
  width: 100%;
  height: 100%;
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  z-index: -1999;
}
</style>
