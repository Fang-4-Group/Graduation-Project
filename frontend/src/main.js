import { createApp } from 'vue';
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconVue from "@element-plus/icons-vue";
import App from './App.vue';
import router from './router';


const app = createApp(App);
for (const [key, component] of Object.entries(ElementPlusIconVue)) {
    app.component(key, component);
}
app.use(ElementPlus);
app.use(router);
app.mount('#app');