<template>
    <div id="app">
      <h1>LIFF App Information</h1>
      <p><strong>OS:</strong> {{ os }}</p>
      <p><strong>Language:</strong> {{ language }}</p>
      <p><strong>LIFF Version:</strong> {{ liffVersion }}</p>
      <p><strong>LINE Version:</strong> {{ lineVersion }}</p>
      <p><strong>Access Token:</strong> {{ accessToken }}</p>
      <p><strong>ID Token:</strong> {{ idToken }}</p>
      <p><strong>Is in LINE Client:</strong> {{ isInClient }}</p>
      <p><strong>Profile:</strong> {{ profile ? profile.displayName : 'Loading...' }}</p>
    </div>
</template>

<script>
  import liff from '@line/liff'

  export default {
    name: 'App',
    data() {
      return {
        os: '',
        language: '',
        liffVersion: '',
        lineVersion: '',
        accessToken: '',
        idToken: '',
        isInClient: false,
        profile: null
      }
    },
    async mounted() {
      try {
        const liffId = '2004824431-BkAJ49jn';
        await liff.init({ liffId });

        if (!liff.isLoggedIn()) {
          liff.login();
        }

        this.os = liff.getOS();
        this.language = navigator.language;
        this.liffVersion = liff.getVersion();
        this.lineVersion = liff.getLineVersion();
        this.accessToken = liff.getAccessToken();
        this.idToken = liff.getIDToken();
        this.isInClient = liff.isInClient();
        this.profile = await liff.getProfile();
      } catch (err) {
        console.error('LIFF initialization failed', err);
      }
    }
  }
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>
