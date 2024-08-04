import { createRouter, createWebHistory } from 'vue-router'; 
import FirstPage from '../components/FirstPage.vue';
import HomeYoung from '../components/HomeYoung.vue'; 
import HomeOld from '../components/HomeOld.vue'; 
import EditBasic from '../components/EditBasic.vue'; 
import EditHousePref from '../components/EditHousePref.vue';
import EditInterests from '../components/EditInterests.vue'; 
import EditPersonality from '../components/EditPersonality.vue'; 
import EditHouseFurniture from'../components/EditHouseFurniture.vue' ;
import EditHouseTraffic from'../components/EditHouseTraffic.vue' ;
import EditHouseBasic from'../components/EditHouseBasic.vue' ;
import LIFF from '../components/LIFF.vue'; 
import UpdateYoung from '@/components/UpdateYoung.vue';
import UpdateOld from '@/components/UpdateOld.vue';

const routes = [
  {path: '/', component: FirstPage },
  { path: '/homeyoung', component: HomeYoung },
  { path: '/homeold', component: HomeOld },
  { path: '/editbasic', component: EditBasic },
  { path: '/editpersonality', component: EditPersonality },
  { path: '/editinterests', component: EditInterests },
  { path: '/edithousepref', component: EditHousePref },
  { path: '/liff', component: LIFF },
  { path: '/edithousefur', component: EditHouseFurniture },
  { path: '/edithousetraf', component: EditHouseTraffic },
  { path: '/edithousebasic', component: EditHouseBasic },
  { path: '/updateyoung', component: UpdateYoung },
  { path: '/updateold', component: UpdateOld }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router; // 導出路由器