<template>
    <div class="container">
      <h1 class="user-info">呈現給別人看的用戶資訊(青)</h1>
      
      <!-- Add Image Section -->
      <div class="header-left">
        <!--<img src="path_to_your_image.jpg" alt="Your Image" class="header-image">-->
      </div>
  
      <!-- User Info Section -->
      <div class="section-boxed">
        <h2>基本資料</h2>
        <div class="user-info-details">
          <div class="data-item">
            <div class="data-item-content">
              <label>姓名：</label>
              <span class="data-value">{{ name }}</span>
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
        <h2>生活習慣</h2>
        <div class="data-item">
          <div class="data-item-content">
            <label>睡覺時間：</label>
            <span class="data-value">{{ sleepTime }}</span>
          </div>
          <div class="data-item-content">
            <label>飲酒程度：</label>
            <span class="data-value">{{ drink }}</span>
          </div>
          <div class="data-item-content">
            <label>抽菸程度：</label>
            <span class="data-value">{{ smoke }}</span>
          </div>
          <div class="data-item-content">
            <label>愛乾淨程度：</label>
            <span class="data-value">{{ clean_habit }}</span>
          </div>
        </div>
      </div>
  
      <!-- Personality Traits Section -->
      <div class="section-boxed">
        <h2>個人特質 </h2>
        <ul class="traits-list">
          <li v-for="trait in characters" :key="trait">{{ trait }}</li>
          <li>{{ mbti }}</li>
        </ul>
      </div>
  
      <!-- Interests Section -->
      <div class="section-boxed">
        <h2>興趣</h2>
        <ul class="interests-list">
          <li v-for="interest in interests" :key="interest">{{ interest }}</li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';
  
  const route = useRoute();
  const People_ID = route.query.People_ID;
  
  const name = ref();
  const useremail = ref("kevin@gmail.com");
  
  const drink = ref("");
  const smoke = ref("");
  const clean_habit = ref("");
  const sleepTime = ref("");
  const characters = ref([]);
  const interests = ref([]);
  const mbti = ref();
  const BASE_URL = 'http://localhost:7877';
  
  onMounted(async () => {
    try {
      const name_Response = await axios.get(`${BASE_URL}/get_name/${People_ID}`); 
      name.value = name_Response.data.name;
  
      const sleep_Response = await axios.get(`${BASE_URL}/get_sleep_time/${People_ID}`);
      const s= sleep_Response.data.sleep_time;
      sleepTime.value = mapSleepTime(s);
  
      const drink_Response = await axios.get(`${BASE_URL}/get_drink/${People_ID}`);
      const d = drink_Response.data.drink;
      drink.value = mapDrinkLevel(d);
  
      const smoke_Response = await axios.get(`${BASE_URL}/get_smoke/${People_ID}`);
      const sm = smoke_Response.data.smoke;
      smoke.value = mapSmokeLevel(sm);
  
      const clean_habit_Response = await axios.get(`${BASE_URL}/get_clean_habit/${People_ID}`);
      const c = clean_habit_Response.data.clean_habit;
      clean_habit.value = mapCleanHabit(c);
  
      const characters_Response = await axios.get(`${BASE_URL}/get_characters/${People_ID}`);
      characters.value = characters_Response.data.characters;
  
      const interests_Response = await axios.get(`${BASE_URL}/get_interests/${People_ID}`);
      interests.value = interests_Response.data.interests;
  
      const mbti_Response = await axios.get(`${BASE_URL}/get_mbti/${People_ID}`);
      mbti.value = mbti_Response.data.mbti;
  
    } catch (error) {
      console.error('Error fetching user information:', error);
    }
  });
  
  function mapSleepTime(s) {
    const times = [
      "晚上7:00~9:00",
      "晚上9:00~11:00",
      "晚上11:00~凌晨1:00",
      "凌晨1:00~3:00",
      "凌晨3:00以後"
    ];
    return times[s - 1] || "未知";
  }
  
  function mapDrinkLevel(d) {
    const levels = [
      "從不飲酒",
      "很少飲酒",
      "偶爾小酌",
      "經常飲酒",
      "每天飲酒"
    ];
    return levels[d] || "未知";
  }
  
  function mapSmokeLevel(sm) {
    const levels = [
      "從不抽菸",
      "很少抽菸",
      "偶爾抽菸",
      "經常抽菸",
      "每天抽菸"
    ];
    return levels[sm] || "未知";
  }
  
  function mapCleanHabit(c) {
    const habits = [
      "不愛乾淨",
      "稍微愛乾淨",
      "正常愛乾淨",
      "很愛乾淨",
      "極度潔癖"
    ];
    return habits[c - 1] || "未知";
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
    display: flex;
    flex-direction: column;
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
  
  .header-left {
    text-align: left;
    margin-bottom: 20px;
  }
  
  .header-image {
    width: 100%;
    max-width: 200px;
  }
  </style>
  