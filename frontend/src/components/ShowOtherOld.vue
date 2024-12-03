<template>
    <div class="container">
      <h1 class="user-info">呈現給別人看的用戶資訊(銀)</h1>
      
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
        <h2>個人特質</h2>
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
  
      <!-- House Basic Info -->
      <div class="section-boxed">
        <h3>房屋資本資料</h3>
        <ul class="house-list">
          <li>房屋大小：{{ size }}</li>
          <li>是否可開火：{{ fire }}</li>
          <li>是否可議價：{{ canNegotiate }}</li>
          <li>城市：{{ city }}</li>
          <li>行政區：{{ district }}</li>
          <li>路名：{{ street }}</li>
          <li>樓層：{{ floor }}</li>
          <li>房屋類別：{{ houseType }}</li>
        </ul>
      </div>
  
      <!-- House Furniture -->
      <div class="section-boxed">
        <h3>房屋家具</h3>
        <ul class="furniture-list">
          <li v-for="(item, index) in houseFurniture" :key="index">{{ item }}</li>
        </ul>
      </div>
  
      <!-- House Traffic -->
      <div class="section-boxed">
        <h3>房屋交通</h3>
        <ul class="traffic-list">
          <li v-for="(item, index) in houseTraffic" :key="index">{{ item }}</li>
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
  
  const name = ref("");
  const useremail = ref("jony12@gmail.com");
  
  const drink = ref("");
  const smoke = ref("");
  const clean_habit = ref("");
  const sleepTime = ref("");
  const characters = ref([]);
  const interests = ref([]);
  const mbti = ref();
  const size = ref(0);
  const fire = ref('');
  const canNegotiate = ref('');
  const city = ref("");
  const district = ref("");
  const street = ref("");
  const floor = ref(0);
  const houseType = ref();
  const houseFurniture = ref([]);
  const houseTraffic = ref([]);
  const BASE_URL = 'https://fang5-group.tw';
  
  onMounted(async () => {
    try {
      const name_Response = await axios.get(`${BASE_URL}/get_name/${People_ID}`); 
      name.value = name_Response.data.name;
  
      const sleep_Response = await axios.get(`${BASE_URL}/get_sleep_time/${People_ID}`);
      const s = sleep_Response.data.sleep_time;
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
  
      const size_Response = await axios.get(`${BASE_URL}/get_size/${People_ID}`);
      size.value = size_Response.data.size;
  
      const fire_Response = await axios.get(`${BASE_URL}/get_fire/${People_ID}`);
      fire.value = fire_Response.data.fire == 1 ? '是' : '否';
  
      const canNegotiate_Response = await axios.get(`${BASE_URL}/get_negotiate/${People_ID}`);
      canNegotiate.value = canNegotiate_Response.data.negotiate_price == 1 ? '是' : '否';
  
      const city_Response = await axios.get(`${BASE_URL}/get_city/${People_ID}`);
      city.value = city_Response.data.city;
  
      const district_Response = await axios.get(`${BASE_URL}/get_district/${People_ID}`);
      district.value = district_Response.data.district;
  
      const street_Response = await axios.get(`${BASE_URL}/get_street/${People_ID}`);
      street.value = street_Response.data.street;
  
      const floor_Response = await axios.get(`${BASE_URL}/get_floor/${People_ID}`);
      floor.value = floor_Response.data.floor;
  
      const houseType_Response = await axios.get(`${BASE_URL}/get_house_type/${People_ID}`);
      houseType.value = houseType_Response.data.type;
  
      const houseFurniture_Response = await axios.get(`${BASE_URL}/get_house_furniture/${People_ID}`);
      houseFurniture.value = houseFurniture_Response.data.furniture;
  
      const houseTraffic_Response = await axios.get(`${BASE_URL}/get_house_traffic/${People_ID}`);
      houseTraffic.value = houseTraffic_Response.data.traffic;
  
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
  display: flex;
  justify-content: center; 
  margin-bottom: 20px; 
}

.section-boxed {
  background-color: #f5f5f5;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column; /* 使內容垂直排列 */
  position: relative; /* 使 .add-button 能夠定位在右側 */
  margin-bottom: 20px; /* 增加下邊距 */
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
.interests-list li,
.furniture-list li,
.traffic-list li,
.house-list li{
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

.housing-info {
  margin-top: 20px;
}

.housing-info h3 {
  margin-bottom: 10px;
}

.header-left {
  text-align: left;
  margin-bottom: 20px;
}
.header-right {
  text-align: right;
  margin-bottom: 20px;
}

.header-image {
  width: 100%;
  max-width: 200px; /* Adjust max-width as needed */
}

.add-button {
  padding: 8px 16px;
  background-color: #606973;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  transition: background-color 0.3s ease;
}

.add-button:hover {
  background-color: #0056b3;
}
</style>
  