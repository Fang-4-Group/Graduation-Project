<template>
  <div class="container">
    <h1 class="user-info">用戶(年輕人)資訊</h1>

    <!-- Add Image Section -->
    <div class="header">
      <img src="path_to_your_image.jpg" alt="Your Image" class="header-image">
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
      <h2>生活習慣 <button class="add-button" @click="goToPage('/editbasic')">新增</button></h2>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import router from '../router';
import { useRoute } from 'vue-router';

const route = useRoute();
const People_ID = route.query.People_ID;

const name = ref()
const useremail = ref("kevin@gmail.com")

const drink = ref("");
const smoke = ref("");
const clean_habit = ref("");
const sleepTime = ref("");
const characters = ref([]);
const interests = ref([]);
const mbti = ref();
const preference_furniture = ref([]);
const preference_house_place = ref([]);
const BASE_URL = 'http://localhost:7877';


onMounted(async () => {
  try {

    const name_Response = await axios.get(`${BASE_URL}/get_name/${People_ID}`);
    name.value = name_Response.data.name;
    console.log("Name data fetched:", name_Response.data);

    const sleep_Response = await axios.get(`${BASE_URL}/get_sleep_time/${People_ID}`);
    const s= sleep_Response.data.sleep_time;
    if(s == 1){
      sleepTime.value = "晚上7:00~9:00";
    }else if(s == 2){
      sleepTime.value = "晚上9:00~11:00";
    }else if(s == 3){
      sleepTime.value = "晚上11:00~凌晨1:00";
    }else if(s == 4){
      sleepTime.value ="凌晨1:00~3:00";
    }else if(s == 5){
      sleepTime.value = "凌晨3:00以後";
    }

    const drink_Response = await axios.get(`${BASE_URL}/get_drink/${People_ID}`);
    const d = drink_Response.data.drink;
      if(d == 0){
        drink.value = "從不飲酒";
      }else if(d == 1){
        drink.value = "很少飲酒";
      }else if(d == 2){
        drink.value = "偶爾小酌";
      }else if(d == 3){
        drink.value = "經常飲酒";
      }else if(d == 4){
        drink.value ="每天飲酒";
      }

    const smoke_Response = await axios.get(`${BASE_URL}/get_smoke/${People_ID}`);
    const sm = smoke_Response.data.smoke;
    if(sm == 0){
      smoke.value = "從不抽菸";
    }else if(sm == 1){
      smoke.value = "很少抽菸";
    }else if(sm == 2){
      smoke.value = "偶爾抽菸";
    }else if(sm == 3){
      smoke.value = "經常抽菸";
    }else if(sm == 4){
      smoke.value ="每天抽菸";
    }


    const clean_habit_Response = await axios.get(`${BASE_URL}/get_clean_habit/${People_ID}`);
    const c = clean_habit_Response.data.clean_habit;
    if(c == 1){
      clean_habit.value = "不愛乾淨";
    }else if(c == 2){
      clean_habit.value = "稍微愛乾淨";
    }else if(c == 3){
      clean_habit.value = "正常愛乾淨";
    }else if(c == 4){
      clean_habit.value ="很愛乾淨";
    }else if(c == 5){
      clean_habit.value = "極度潔癖";
    }

    const characters_Response = await axios.get(`${BASE_URL}/get_characters/${People_ID}`);
    characters.value = characters_Response.data.characters;

    const interests_Response = await axios.get(`${BASE_URL}/get_interests/${People_ID}`);
    interests.value = interests_Response.data.interests;

    const mbti_Response = await axios.get(`${BASE_URL}/get_mbti/${People_ID}`);
    mbti.value = mbti_Response.data.mbti;

    const preference_furniture_Response = await axios.get(`${BASE_URL}/get_preference_furniture/${People_ID}`);
    preference_furniture.value = preference_furniture_Response.data.message;

    const preference_house_place_Response = await axios.get(`${BASE_URL}/get_preference_house_place/${People_ID}`);
    preference_house_place.value = preference_house_place_Response.data.message;

  } catch (error) {
    console.error('Error fetching user information:', error);
  }
});

function goToPage(path) {
    router.push({ path, query: { from: '/homeyoung' } });
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
  max-width: 200px;
}

.add-button {
  float: right;
  margin-top: -10px;
}
</style>
