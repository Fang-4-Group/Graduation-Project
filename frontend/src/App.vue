<template>
<<<<<<< HEAD
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
  <LIFF></LIFF>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import LIFF from './components/LIFF.vue'


export default {
  name: 'App',
  components: {
    HelloWorld,
    LIFF
  }
}
=======
  <div id="app">
    <!--<Home></Home>-->
    <router-view></router-view>
    <!--<Edit></Edit>-->
    <div :class="userData"></div>
  </div>
</template>

<script setup>
//import Home from "./components/Home.vue";
//import Edit from "./components/Edit.vue";

>>>>>>> c758ff6 (add apis)
</script>

<style>
#app {
  margin: 20px;
}
nav {
  margin-bottom: 20px;
}
</style>