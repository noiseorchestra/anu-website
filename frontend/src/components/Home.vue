<template>
  <div class="home-container">
    <div @click="shouldShowLogo = false">
      <BackgroundLogo v-if="shouldShowLogo" />
      <div v-else>
        <div>
          <AnuSkyGod />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BackgroundLogo from "@/components/BackgroundLogo.vue";
import AnuSkyGod from "@/components/AnuSkyGod.vue";

export default {
  name: "Home",
  components: {
    BackgroundLogo,
    AnuSkyGod,
  },
  data() {
    return { shouldShowLogo: true };
  },
};
</script>

<style scoped lang="scss">
.home-container {
  display: flex;
  align-items: flex-end;
  justify-content: center;
}
</style>
