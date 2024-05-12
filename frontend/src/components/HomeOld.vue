<template>
    <div class="container">
      <h1 class="user-info">用戶(老人)資訊</h1>
       <!-- Add Image Section -->
    <div class="header">
      <img src="path_to_your_image.jpg" alt="Your Image" class="header-image">
    </div>

    <!-- User Info Section -->
    <div class="section-boxed">
      <h2>基本資料</h2>
      
        <div class="data-item">
          <label>姓名：</label>
          <span class="data-value">{{ username }}</span>
        </div>
        <div class="data-item">
          <label>信箱：</label>
          <span class="data-value">{{ useremail }}</span>
        </div>
     
    </div>
  
      <!-- Basic Info Section -->
      <div class="section-boxed">
        <h2>
          生活習慣
          <button @click="goToPage('/editbasic')">新增</button>
        </h2>
        <div class="data-item">
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
  
        <!-- 房屋資本資料 -->
        <div class="section-boxed">
          <h3>房屋資本資料</h3>
          <ul class="house-list">
            <li>房屋大小：{{ houseCapital.size }}</li>
            <li>是否可開火：{{ houseCapital.canCook }}</li>
            <li>是否可議價：{{ houseCapital.canNegotiate }}</li>
            <li>地址：{{ houseCapital.address }}</li>
            <li>樓層：{{ houseCapital.floor }}</li>
            <li>房屋類別：{{ houseCapital.houseType }}</li>
          </ul>
        </div>
  
        <!-- 房屋家具 -->
        <div class="section-boxed">
          <h3>房屋家具</h3>
          <ul class="furniture-list">
            <li v-for="(item, index) in houseFurniture" :key="index">{{ item }}</li>
          </ul>
        </div>
  
        <!-- 房屋交通 -->
        <div class="section-boxed">
          <h3>房屋交通</h3>
          <ul class="traffic-list">
            <li v-for="(item, index) in houseTransportation" :key="index">{{ item }}</li>
          </ul>
        </div>
      </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import router from '../router'; // 實際路徑

  const username = ref("老王")
  const useremail = ref("1234@gmail.com")
  
  const userData = ref({
    basicInfo: {
      sleepTime: 9,
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
  
  const houseCapital = ref({
    size: '10坪',
    canCook: '是',
    canNegotiate: '是',
    address: '台北市中山區118巷',
    floor: '4樓',
    houseType: '透天厝'
  });
  const houseFurniture = ref(['桌子', '餐桌', '冷氣']);
  const houseTransportation = ref(['近捷運', '近公車站']);
  
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
  justify-content: center; /* 水平置中 */
  margin-bottom: 20px; /* 調整下方間距 */
}

.section-boxed {
  background-color: #f5f5f5; /* 淺灰色 */
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
.interests-list li,
.furniture-list li,
.traffic-list li,
.house-list li{
  margin-right: 10px;
  margin-bottom: 5px;
  padding: 5px 10px;
  border-radius: 20px;
  background-color: #c2d4dc; /* 淡藍色 */
  color: #333;
  display: inline-block;
}

.data-value {
  margin-right: 10px;
  margin-bottom: 5px;
  padding: 5px 10px;
  border-radius: 20px;
  background-color: #d9b9b0; /* 淡粉色 */
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
  background-color: #c2d4dc; /* 淡藍色 */
  color: #333;
  margin-right: 10px;
  margin-bottom: 10px;
}

.housing-info {
  margin-top: 20px;
}

.housing-info h3 {
  margin-bottom: 10px;
}

.header {
  text-align: left;
  margin-bottom: 20px;
}

.header-image {
  width: 100%;
  max-width: 200px; /* Adjust max-width as needed */
}
</style>