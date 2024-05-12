import { createRouter, createWebHistory } from 'vue-router'; // 導入創建路由器的函數
import Home from '../components/HomeYoung.vue'; // 導入首頁(年輕人)組件
import HomeOld from '../components/HomeOld.vue'; // 導入首頁(老人)組件
import EditBasic from '../components/EditBasic.vue'; // 導入編輯頁面組件
import EditHousePref from '../components/EditHousePref.vue'; // 導入編輯頁面組件
import EditInterests from '../components/EditInterests.vue'; // 導入編輯頁面組件
import EditPersonality from '../components/EditPersonality.vue'; // 導入編輯頁面組件

const routes = [
  { path: '/', component: Home },
  { path: '/homeold', component: HomeOld },
  { path: '/editbasic', component: EditBasic },
  { path: '/editpersonality', component: EditPersonality },
  { path: '/editinterests', component: EditInterests },
  { path: '/edithousepref', component: EditHousePref },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router; // 導出路由器