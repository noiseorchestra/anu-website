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
      let ANU_BLACK;
      let CAM_FRAG;
      let CRYS_FRAG;
      let LIGHT_FRAG;
      let MILL_FRAG;
      let ORANGE_FRAG;
      let SHAPE_FRAG;
      let TEXT;

      let fr = .5;

      s.preload = () => {
        ANU_BLACK = s.loadImage (require('../../assets/ANU_BLACK.png'));
        CAM_FRAG = s.loadImage(require('../../assets/CAM_FRAG.png'));
        CRYS_FRAG = s.loadImage (require('../../assets/CRYS_FRAG.png'));
        LIGHT_FRAG = s.loadImage (require('../../assets/LIGHT_FRAG.png'));
        MILL_FRAG = s.loadImage (require('../../assets/MILL_FRAG.png'));
        ORANGE_FRAG = s.loadImage (require('../../assets/ORANGE_FRAG.png'));
        SHAPE_FRAG = s.loadImage (require('../../assets/SHAPE_FRAG.png'));
        TEXT = s.loadImage (require('../../assets/TEXT.png'));
      }

      s.setup = () => {
        s.createCanvas(window.innerWidth, window.innerHeight);
        s.frameRate(fr);
      }

      s.draw = () => {
        s.background(254,208,22); //yellow
        s.background(0);
        s.imageMode(s.CENTER);
        s.image (ANU_BLACK,window.innerWidth/2,260);
        s.image (TEXT, window.innerWidth/2,460);
        s.image (CAM_FRAG, s.random(600),s.random (500),150,150)
        s.image (CRYS_FRAG,s.random(800),s.random(600),100,100);
        s.image (LIGHT_FRAG,s.random(800),s.random(600),150,150);
        s.image (MILL_FRAG,s.random(800),s.random(600),150,150);
        s.image (ORANGE_FRAG,s.random(800),s.random(600),200,200);
        s.image (SHAPE_FRAG,s.random(800),s.random(600),100,100);
      }
    }
    let canvas = new P5(sketch, 'canvas');
  }
}

</script>

<style>
#canvas {
  overflow: hidden;
  max-width: 100vw;
  max-height: 100vh;
}
</style>
