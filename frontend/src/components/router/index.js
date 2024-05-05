import { createRouter, createWebHistory } from 'vue-router'; // 導入創建路由器的函數
import Home from '../Home.vue'; // 導入首頁組件
import Edit from '../Edit.vue'; // 導入編輯頁面組件

const router = createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/home', component: Home },
      { path: '/edit', component: Edit },
    ],
  });

export default router; // 導出路由器
