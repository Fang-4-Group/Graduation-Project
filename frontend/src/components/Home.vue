<template>
  <div class="container">
    <h1 class="user-info">用戶資訊</h1>

    <!-- Basic Info Section -->
    <div class="section-boxed">
      <h2>
        基本資料
        <button @click="goToPage('/editbasic')">新增</button>
      </h2>
      <div class="data-item">
        <label>睡覺時間：</label>
        <span class="data-value">{{ sleepTime }}</span>
      </div>
      <div class="data-item">
        <label>菸酒程度：</label>
        <span class="data-value">{{ drink_or_smoke }}</span>
        <label>愛乾淨程度：</label>
        <span class="data-value">{{ clean_habit }}</span>
      </div>
    </div>

    <!-- Personality Traits Section -->
    <div class="section-boxed">
      <h2>
        個人特質
        <button @click="goToPage('/editpersonality')">新增</button>
      </h2>
      <ul class="traits-list">
        <li v-for="trait in characters" :key="trait">{{ trait }}</li>
        <li>{{ mbti }}</li>
      </ul>
    </div>

    <!-- Interests Section -->
    <div class="section-boxed">
      <h2>
        興趣
        <button @click="goToPage('/editinterests')">新增</button>
      </h2>
      <ul class="interests-list">
        <li v-for="interest in interests" :key="interest">{{ interest }}</li>
      </ul>
    </div>

    <!-- Housing Preferences Section -->
    <div class="section-boxed">
      <h2>
        房屋偏好
        <button @click="goToPage('/edithousepref')">新增</button>
      </h2>
      <div class="furniture-list">
        <div v-for="(item, index) in preference_furniture" :key="index" class="furniture-item">
          {{ item }}
        </div>
        <div v-for="(item, index) in preference_house_place" :key="index" class="furniture-item">
          {{ item }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import router from './router'; // 实际路径 

const drink_or_smoke = ref(0);
const clean_habit = ref(0);
const sleepTime = ref(0);
const characters = ref([]);
const interests = ref([]);
const mbti = ref();
const preference_furniture = ref([]);
const preference_house_place = ref([]);
const BASE_URL = 'http://localhost:8000';


// 发送HTTP请求获取用户信息
onMounted(async () => {
  try {
    const sleep_Response = await axios.get(`${BASE_URL}/get_sleep_time/1`); // 假设传入的people_id为1
    sleepTime.value = sleep_Response.data.sleep_time;

    const drink_or_smoke_Response = await axios.get(`${BASE_URL}/get_drink_or_smoke/1`); // 假设传入的people_id为1
    drink_or_smoke.value = drink_or_smoke_Response.data.drink_or_smoke;

    const clean_habit_Response = await axios.get(`${BASE_URL}/get_clean_habit/1`); // 假设传入的people_id为1
    clean_habit.value = clean_habit_Response.data.clean_habit;

    const characters_Response = await axios.get(`${BASE_URL}/get_characters/1`); // 假设传入的people_id为1
    characters.value = characters_Response.data.characters;

    const interests_Response = await axios.get(`${BASE_URL}/get_interests/1`); // 假设传入的people_id为1
    interests.value = interests_Response.data.interests; 

    const mbti_Response = await axios.get(`${BASE_URL}/get_mbti/1`); // 假设传入的people_id为1
    mbti.value = mbti_Response.data.mbti;

    const preference_furniture_Response = await axios.get(`${BASE_URL}/get_preference_furniture/1`); // 假设传入的preference_id为1
    preference_furniture.value = preference_furniture_Response.data.message; // 

    const preference_house_place_Response = await axios.get(`${BASE_URL}/get_preference_house_place/1`); // 假设传入的preference_id为1
    preference_house_place.value = preference_house_place_Response.data.message; // 此处修正为正确的变量名

  } catch (error) {
    console.error('Error fetching user information:', error);
  }
});

function goToPage(path) {
  router.push(path);
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.user-info {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.section-boxed {
  background-color: #f5f5f5;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
}

.data-item {
  display: flex;
  margin-bottom: 10px;
}

.data-item label {
  font-weight: bold;
  margin-right: 10px;
}

.traits-list,
.interests-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.traits-list li,
.interests-list li {
  margin-right: 10px;
  margin-bottom: 5px;
  padding: 5px 10px;
  border-radius: 20px;
  background-color: #c2d4dc;
  color: #333;
  display: inline-block;
}

.data-value {
  margin-right: 10px;
  margin-bottom: 5px;
  padding: 5px 10px;
  border-radius: 20px;
  background-color: #d9b9b0;
  color: #333;
  display: inline-block;
}

.furniture-list {
  display: flex;
  flex-wrap: wrap;
}

.furniture-item {
  padding: 5px 10px;
  border-radius: 20px;
  background-color: #c2d4dc;
  color: #333;
  margin-right: 10px;
  margin-bottom: 10px;
}
</style>
