import { createRouter, createWebHistory } from 'vue-router'; // 導入創建路由器的函數
import Home from '../Home.vue'; // 導入首頁組件
import EditBasic from '../EditBasic.vue'; // 導入編輯頁面組件
import EditHousepref from '../EditHousepref.vue'; // 導入編輯頁面組件
import EditInterests from '../EditInterests.vue'; // 導入編輯頁面組件
import EditPersonality from '../EditPersonality.vue'; // 導入編輯頁面組件

// const router = createRouter({
//     history: createWebHistory(),
//     routes: [
//       { path: '/home', component: Home },
//       { path: '/edit', component: Edit },
//     ],
//   });
const routes = [
  { path: '/', component: Home },
  { path: '/editbasic', component: EditBasic },
  { path: '/editpersonality', component: EditPersonality },
  { path: '/editinterests', component: EditInterests },
  { path: '/edithousepref', component: EditHousepref },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router; // 導出路由器
