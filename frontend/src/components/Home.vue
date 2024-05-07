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
        <label>年齡：</label>
        <span class="data-value">{{ userData.basicInfo.age }}</span>
        <label>睡覺時間：</label>
        <span class="data-value">{{ userData.basicInfo.sleepTime }}</span>
      </div>
      <div class="data-item">
        <label>菸酒程度：</label>
        <span class="data-value">{{ userData.basicInfo.alcoholLevel }}</span>
        <label>愛乾淨程度：</label>
        <span class="data-value">{{ userData.basicInfo.cleanlinessLevel }}</span>
      </div>
    </div>

    <!-- Personality Traits Section -->
    <div class="section-boxed">
      <h2>
        個人特質
        <button @click="goToPage('/editpersonality')">新增</button>
      </h2>
      <ul class="traits-list">
        <li v-for="trait in userData.personalityTraits" :key="trait">{{ trait }}</li>
      </ul>
    </div>

    <!-- Interests Section -->
    <div class="section-boxed">
      <h2>
        興趣
        <button @click="goToPage('/editinterests')">新增</button>
      </h2>
      <ul class="interests-list">
        <li v-for="interest in userData.interests" :key="interest">{{ interest }}</li>
      </ul>
    </div>

    <!-- Housing Preferences Section -->
    <div class="section-boxed">
      <h2>
        房屋偏好
        <button @click="goToPage('/edithousepref')">新增</button>
      </h2>
      <div class="furniture-list">
        <div v-for="(item, index) in userData.housingPreferences.furniture" :key="index" class="furniture-item">
          {{ item }}
        </div>
        <div v-for="(item, index) in userData.housingPreferences.district" :key="index" class="furniture-item">
          {{ item }}
        </div>
      </div>
  </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import router from './router'; // 实际路径 
const userData = ref({
  basicInfo: {
    age: 19,
    sleepTime: 3,
    alcoholLevel: 2,
    cleanlinessLevel: 1
  },
  personalityTraits: ['Mbti', '友善', '負責任', '玻璃心', '體貼'],
  interests: ['音樂', '旅行', '遊戲', '睡覺', '吃飯', '唱歌', '跳繩'],
  housingPreferences: {
    district: ['中山區', '大同區'],
    furniture: ['床', '書桌', '椅子']
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
  justify-content: center; /* 水平居中 */
  margin-bottom: 20px; /* 調整下方間距 */
}

.user-info img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}

.section {
  margin-top: 30px;
}

.section-boxed {
  background-color: #f5f5f5; /* Light gray */
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
  background-color: #c2d4dc; /* 莫蘭迪淡藍色 */
  color: #333;
  display: inline-block;
}

.data-value {
  margin-right: 10px;
  margin-bottom: 5px;
  padding: 5px 10px;
  border-radius: 20px;
  background-color: #d9b9b0; /* 莫蘭迪淡粉色 */
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
  background-color: #c2d4dc; /* 莫蘭迪淡藍色 */
  color: #333;
  margin-right: 10px;
  margin-bottom: 10px;
}
</style>