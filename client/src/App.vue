<template>
  <div class="q-app">
    <router-view />
  </div>
</template>

<style lang="scss">
html,
body,
#app,
.q-app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

* {
  font-family: Gilroy, Avenir, Helvetica, Arial, sans-serif;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
