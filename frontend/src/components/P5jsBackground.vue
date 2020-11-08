<template>
    <div id="canvas"></div>
</template>

<script>
import P5 from 'p5'

export default {
  name: 'P5jsBackground',
  data: function() {
    return {pages: {}}
  },
  created: function () {
    const sketch = s => {
      let fr = 3;

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
        SHUKOV = s.loadImage (require('../../assets/SHUKOV.png'));
        METRO = s.loadImage (require('../../assets/METRO.png'))
        ORANGE = s.loadImage (require('../../assets/ORANGE.png'));
        CACTUS = s.loadImage (require('../../assets/CACTUS.png'));
        CAM = s.loadImage (require('../../assets/CAM.png'));
        COSMOS =s.loadImage (require('../../assets/COSMOS.png'));
        CRYS = s.loadImage (require('../../assets/CRYS.png'));
        MILL = s.loadImage (require('../../assets/MILL.png'));
        MOSCOW = s.loadImage (require('../../assets/MOSCOW.png'));
        LIGHT = s.loadImage (require('../../assets/LIGHT.png'));
        HIRO = s.loadImage (require('../../assets/HIRO.png'));
        TABLET = s.loadImage (require('../../assets/TABLET.png'));
        STONE = s.loadImage (require('../../assets/STONE.png'));
      }

      s.setup = () => {
        s.createCanvas(window.innerWidth, window.innerHeight);
        s.frameRate(fr);
      }

      s.draw = () => {
        s.background (0);
        s.image(SHUKOV,s.random(window.innerWidth),s.random(window.innerHeight),180,180);
        s.image (METRO,s.random(window.innerWidth),s.random(window.innerHeight),200,180);
        s.image (ORANGE,s.random(window.innerWidth),s.random(window.innerHeight),150,150);
        s.image (CACTUS, s.random (window.innerWidth),s.random(window.innerHeight),200,200);
        s.image (CAM, s.random (window.innerWidth),s.random(window.innerHeight),200,200);
        s.image (COSMOS, s.random (window.innerWidth),s.random(window.innerWidth),200,200);
        s.image (CRYS,s.random (window.innerWidth),s.random(window.innerWidth),200,200);
        s.image (MILL,s.random (window.innerWidth),s.random(window.innerWidth),200,200);
        s.image (MOSCOW,s.random (window.innerWidth),s.random(window.innerWidth),200,200);
        s.image (LIGHT,s.random (window.innerWidth),s.random(window.innerWidth),200,200);
        s.image (HIRO,s.random (window.innerWidth),s.random(window.innerWidth),300,285);
        s.image (TABLET,s.random (window.innerWidth),s.random(window.innerWidth),200,200);
        s.image (STONE,s.random (window.innerWidth),s.random(window.innerWidth),170,230);
      }
    }
    let canvas = new P5(sketch, 'canvas');
  }
}

</script>

<style scoped>
#canvas {
  width: 100%;
  height: 100%;
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  z-index: -9999;
}
</style>
