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
  
        <!-- House Basic Info -->
        <div class="section-boxed">
          <h3>房屋資本資料<button class="add-button" @click="goToPage('/edithousebasic')">新增</button></h3>
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
          <h3>房屋家具<button class="add-button" @click="goToPage('/edithousefur')">新增</button></h3>
          <ul class="furniture-list">
            <li v-for="(item, index) in houseFurniture" :key="index">{{ item }}</li>
          </ul>
        </div>
  
        <!-- House Traffic-->
        <div class="section-boxed">
          <h3>房屋交通<button class="add-button" @click="goToPage('/edithousetraf')">新增</button></h3>
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
  import { useRoute } from 'vue-router';

  const route = useRoute();
  const People_ID = route.query.People_ID;


  const name = ref("")
  const useremail = ref("jony12@gmail.com")

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
        sleepTime.value = "晚上11:00~隔天1:00";
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
      }else if(d == 5){
        drink.value = "酗酒";
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
      }else if(sm == 5){
        smoke.value = "重度菸癮";
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

      const size_Response = await axios.get(`${BASE_URL}/get_size/${People_ID}`); 
      size.value = size_Response.data.size;

      const fire_Response = await axios.get(`${BASE_URL}/get_fire/${People_ID}`); 
      if (fire_Response.data.fire == 1)
        fire.value='是'
      else
        fire.value='否'

      const canNegotiate_Response = await axios.get(`${BASE_URL}/get_negotiate/${People_ID}`); 
      if (canNegotiate_Response.data.negotiate_price.fire == 1)
        canNegotiate.value='是'
      else
        canNegotiate.value='否'
      
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
 
  
  function goToPage(path) {
    router.push({ path, query: { from: '/HomeOld' } });
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