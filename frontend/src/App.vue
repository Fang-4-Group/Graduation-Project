<template>
  <div id="app">
    <Home></Home>
    <router-view></router-view>
    <!--<Edit></Edit>-->
    <div :class="userData"></div>
  </div>
</template>

<script setup>
import Home from "./components/Home.vue";
//import Edit from "./components/Edit.vue";

</script>

<style>
#app {
  margin: 20px;
}
nav {
  margin-bottom: 20px;
}
</style>