<template>
    <div class="container">
      <h1 class="user-info">用戶(老人)資訊</h1>
       <!-- Add Image Section -->
    <div class="header">
      <img src="path_to_your_image.jpg" alt="Your Image" class="header-image">
    </div>

    <!-- User Info Section -->
    <div class="section-boxed">
      <h2>基本資料<button class="add-button" @click="goToPage('/editbasic')">新增</button></h2>
      
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
          <button class="add-button" @click="goToPage('/editbasic')">新增</button>
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
  
        <!-- 房屋資本資料 -->
        <div class="section-boxed">
          <h3>房屋資本資料</h3>
          <ul class="house-list">
            <li>房屋大小：{{ size }}</li>
            <li>是否可開火：{{ fire }}</li>
            <li>是否可議價：{{ canNegotiate }}</li>
            <li>地址：{{ address }}</li>
            <li>樓層：{{ floor }}</li>
            <li>房屋類別：{{ houseType }}</li>
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
            <li v-for="(item, index) in houseTraffic" :key="index">{{ item }}</li>
          </ul>
        </div>
      </div>
  </template>
  
  <script setup>
  import { ref,onMounted } from 'vue';
  import axios from 'axios';
  import router from '../router'; 

  const username = ref("老王")
  const useremail = ref("1234@gmail.com")

  const drink_or_smoke = ref(0);
  const clean_habit = ref(0);
  const sleepTime = ref(0);
  const characters = ref([]);
  const interests = ref([]);
  const mbti = ref();
  const size = ref(0);
  const fire = ref('');
  const canNegotiate = ref('');
  const address = ref("暫時先寫台北市文山區木柵路123巷");
  const floor = ref(0);
  const houseType = ref();
  const houseFurniture = ref([]);
  const houseTraffic = ref([]);
  const BASE_URL = 'http://localhost:7877';
  
  
  onMounted(async () => {
    try {
      const sleep_Response = await axios.get(`${BASE_URL}/get_sleep_time/3`); 
      sleepTime.value = sleep_Response.data.sleep_time;

      const drink_or_smoke_Response = await axios.get(`${BASE_URL}/get_drink_or_smoke/3`); 
      drink_or_smoke.value = drink_or_smoke_Response.data.drink_or_smoke;

      const clean_habit_Response = await axios.get(`${BASE_URL}/get_clean_habit/3`); 
      clean_habit.value = clean_habit_Response.data.clean_habit;

      const characters_Response = await axios.get(`${BASE_URL}/get_characters/3`); 
      characters.value = characters_Response.data.characters;

      const interests_Response = await axios.get(`${BASE_URL}/get_interests/3`); 
      interests.value = interests_Response.data.interests;

      const mbti_Response = await axios.get(`${BASE_URL}/get_mbti/3`); 
      mbti.value = mbti_Response.data.mbti;

      const size_Response = await axios.get(`${BASE_URL}/get_size/3`); 
      size.value = size_Response.data.size;

      const fire_Response = await axios.get(`${BASE_URL}/get_fire/3`); 
      if (fire_Response.data.fire == 1)
        fire.value='是'
      else
        fire.value='否'

      const canNegotiate_Response = await axios.get(`${BASE_URL}/get_negotiate/3`); 
      if (canNegotiate_Response.data.negotiate_price.fire == 1)
        canNegotiate.value='是'
      else
        canNegotiate.value='否'
      
      const floor_Response = await axios.get(`${BASE_URL}/get_floor/3`);
      floor.value = floor_Response.data.floor;

      const houseType_Response = await axios.get(`${BASE_URL}/get_house_type/3`); 
      houseType.value = houseType_Response.data.type;

      const houseFurniture_Response = await axios.get(`${BASE_URL}/get_house_furniture/3`); 
      houseFurniture.value = houseFurniture_Response.data.furniture; 

      const houseTraffic_Response = await axios.get(`${BASE_URL}/get_house_traffic/3`); 
      houseTraffic.value = houseTraffic_Response.data.traffic; 

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

.add-button {
  float: right;
  margin-top: -10px;
}
</style>