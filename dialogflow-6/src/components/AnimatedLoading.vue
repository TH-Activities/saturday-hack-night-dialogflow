<template>
  <div class="animated-loading" v-if="showAnimatedLoading === true">
    <transition name="fade"> 
        <div class="pulse"></div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "AnimatedLoading",
  props: {
    showAnimatedLoading: {
      default: false,
      type: Boolean,
    },
  },
};
</script>

<style scoped>
.animated-loading {
  background-color: var(--baby-blue-eyes);
  position: fixed;
  top: 0px;
  bottom: 0px;
  left: 0px;
  right: 0px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9;
}

.pulse {
  animation: pulse-animation 2s infinite;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  box-shadow: 0px 0px 1px 1px #0000001a;
  background-color: var(--blush);
}

@keyframes pulse-animation {
  0% {
    box-shadow: 0 0 0 0px rgba(227, 101, 136, 0.2);
  }
  100% {
    box-shadow: 0 0 0 20px rgba(0, 0, 0, 0);
  }
}

/* vue animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>