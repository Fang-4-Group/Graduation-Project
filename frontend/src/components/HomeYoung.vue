<template>
  <div class="container">
    <h1 class="user-info">用戶(年輕人)資訊</h1>
    
    <!-- Add Image Section -->
    <div class="header">
      <img src="path_to_your_image.jpg" alt="Your Image" class="header-image">
    </div>

    <!-- User Info Section -->
    <div class="section-boxed">
      <h2>基本資料 <button class="add-button" @click="goToPage('/editbasic')">新增</button></h2>
      <div class="user-info-details">
        <div class="data-item">
          <div class="data-item-content">
            <label>姓名：</label>
            <span class="data-value">{{ username }}</span>
          </div>
          <div class="data-item-content">
            <label>信箱：</label>
            <span class="data-value">{{ useremail }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Basic Info Section -->
    <div class="section-boxed">
      <h2>生活習慣 <button class="add-button" @click="goToPage('/editbasic')">新增</button></h2>
      <div class="data-item">
        <div class="data-item-content">
          <label>睡覺時間：</label>
          <span class="data-value">{{ sleepTime }}</span>
        </div>
        <div class="data-item-content">
          <label>菸酒程度：</label>
          <span class="data-value">{{ drink_or_smoke }}</span>
        </div>
        <div class="data-item-content">
          <label>愛乾淨程度：</label>
          <span class="data-value">{{ clean_habit }}</span>
        </div>
      </div>
    </div>

    <!-- Personality Traits Section -->
    <div class="section-boxed">
      <h2>個人特質 <button class="add-button" @click="goToPage('/editpersonality')">新增</button></h2>
      <ul class="traits-list">
        <li v-for="trait in characters" :key="trait">{{ trait }}</li>
        <li>{{ mbti }}</li>
      </ul>
    </div>

    <!-- Interests Section -->
    <div class="section-boxed">
      <h2>興趣 <button class="add-button" @click="goToPage('/editinterests')">新增</button></h2>
      <ul class="interests-list">
        <li v-for="interest in interests" :key="interest">{{ interest }}</li>
      </ul>
    </div>

    <!-- Housing Preferences Section -->
    <div class="section-boxed">
      <h2>房屋偏好 <button class="add-button" @click="goToPage('/edithousepref')">新增</button></h2>
      <div class="furniture-list">
        <div v-for="(item, index) in preference_furniture" :key="index" class="furniture-item">{{ item }}</div>
        <div v-for="(item, index) in preference_house_place" :key="index" class="furniture-item">{{ item }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import router from '../router'; // 实际路径

const username = ref("使用者")
const useremail = ref("1234@gmail.com")

const drink_or_smoke = ref(0);
const clean_habit = ref(0);
const sleepTime = ref(0);
const characters = ref([]);
const interests = ref([]);
const mbti = ref();
const preference_furniture = ref([]);
const preference_house_place = ref([]);
const BASE_URL = 'http://localhost:7877';


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
  text-align: center;
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
  flex-direction: column;
  margin-bottom: 10px;
}

.data-item-content {
  text-align: center;
}

.data-item label {
  font-weight: bold;
  margin-right: 10px;
}

.traits-list,
.interests-list,
.furniture-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.traits-list li,
.interests-list li,
.furniture-list li,
.furniture-item {
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

.header {
  text-align: left;
  margin-bottom: 20px;
}

.header-image {
  width: 100%;
  max-width: 200px; /* Adjust max-width as needed */
}

.add-button {
  float: right;
  margin-top: -10px;
}
</style>