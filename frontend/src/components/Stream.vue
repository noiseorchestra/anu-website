<template>
  <div class="page-body" tabindex="0">
    <div class="text-wrapper">
      <div>
        <img id="image-header" alt="ANU Festival of Improvised Music" :src="image" />
        <p>
          Global cast of improvisors meet online via the JackTrip powered Noise Orchestra ANU system, for small and large group improvisation live in real time. With Maggie Nicols, Yan Jun, Fritz Welch, Ikbal Lubys, Tyler Damon, Sam Andreae, David Birchall, Dirar Kalash, Kae San, Odie Ji Ghast, Sasha Elina and Aziz Lewandowski.
        </p>
        
        <p>More info on all artists <a href="/anu-fest/">here</a>.</p>
        <p>More info about ANU <a href="/about-anu/">here</a>.</p>
        
        <h2>live stream</h2>
        <audio
          src="https://icecast.autonomousnoiseunit.co.uk/stream"
          controls="true"
        />
        <p><i>If this stream doesn't seem to work for you, try the <a href="https://icecast.autonomousnoiseunit.co.uk/stream">direct link</a>.</i></p>
        <p><strong>Saturday 4th December 3-5pm GMT</strong></p>
        <p>
          Tyler Damon (Chicago)<br>
          Sasha Elina (Moscow)<br>
          Aziz Lewandowski (Berlin)<br> 
          Maggie Nicols (Carmarthenshire)<br>
        </p>
        <p>
          Greta Buitkute (Newcastle)<br>
          David Birchall (Manchester)<br>
          Ikbal Lubys (Yogyakarta)<br>
          Ali Robertson (Edinburgh)
        </p>
        <p>
          Yan Jun (Beijing)<br>
          Dirar Kalash (Ramallah) <br>
          Kae San (Japan)
          Sam Andreae (London)
        </p>

        <p><strong>Sunday 5th December 3-5pm GMT</strong></p>
        <p>
          2 hours of uninterupted musical collage. All 12 musicians are invited to contribute at any point during this 2 hour session.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageContent',
  data() {
    return {
      image: require('../../assets/ANU_FOIM_crop.png'),
    };
  },
};
</script>

<style scoped lang="scss">
@import '@/scss/_variables.scss';

#image-header {
  max-width: 100%;
}

.page-body {
  overflow-x: hidden;
  background-color: map-get($colors, 'dark');
  min-height: 100%;
  color: map-get($colors, 'bright');
  overflow-y: auto;
  &::-webkit-scrollbar {
    width: 12px;
  }
  &::-webkit-scrollbar-track {
    background: map-get($colors, 'dark');
  }
  &::-webkit-scrollbar-thumb {
    background: map-get($colors, 'bright');
  }
  &::-webkit-scrollbar-thumb:hover {
    background: map-get($colors, 'highlight');
  }
}

.text-wrapper {
  padding: 20px;
  padding-top: 30px;
  color: map-get($colors, 'bright');
}
</style>
