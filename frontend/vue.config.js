const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // For ngrok in the testing stage
  devServer: {
    allowedHosts: 'all',
  }
})



