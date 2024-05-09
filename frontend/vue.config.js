const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
<<<<<<< HEAD
  // For ngrok in the testing stage
  devServer: {
    allowedHosts: 'all',
  }
=======
  // Add this line of code to disable lintOnSave
  lintOnSave: false
  
>>>>>>> c758ff6 (add apis)
})


