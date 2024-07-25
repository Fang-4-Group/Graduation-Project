<template>
  <div class="container">
    <h1>首次登錄</h1>
    <form @submit.prevent="submitForm">
      <!-- Role Selection -->
      <div class="form-group">
        <label style="margin-right: 10px; font-weight: bold;">你是：</label>
        <div style="display: inline-block;">
          <input type="radio" id="young" :value="0" v-model="user_data.Role">
          <label for="young" style="margin-right: 10px;">年輕人</label>
        </div>
        <div style="display: inline-block;">
          <input type="radio" id="old" :value="1" v-model="user_data.Role">
          <label for="old">年長者</label>
        </div>
      </div>

      <!-- Common Fields -->
      <div>
        <div class="form-group">
          <label for="name" style="font-weight: bold;">姓名：</label>
          <input type="text" id="name" v-model="user_data.Name" required>
        </div>
        <div class="form-group">
          <label for="sleepTime" style="font-weight: bold;">睡覺時間：</label>
          <select id="sleepTime" v-model.number="user_data.Sleep_Time" required>
            <option value="1">晚上7:00~9:00</option>
            <option value="2">晚上9:00~11:00</option>
            <option value="3">晚上11:00~凌晨1:00</option>
            <option value="4">凌晨1:00~3:00</option>
            <option value="5">凌晨3:00以後</option>
          </select>
        </div>
        <div class="form-group">
          <label for="drink" style="font-weight: bold;">飲酒程度：</label>
          <select id="drink" v-model.number="user_data.Drink" required>
            <option value="0">從不飲酒</option>
            <option value="1">很少飲酒</option>
            <option value="2">偶爾小酌</option>
            <option value="3">經常飲酒</option>
            <option value="4">每天飲酒</option>
          </select>
        </div>
        <div class="form-group">
          <label for="smoke" style="font-weight: bold;">抽菸程度：</label>
          <select id="smoke" v-model.number="user_data.Smoke" required>
            <option value="0">從不抽菸</option>
            <option value="1">很少抽菸</option>
            <option value="2">偶爾抽菸</option>
            <option value="3">經常抽菸</option>
            <option value="4">每天抽菸</option>
          </select>
        </div>
        <div class="form-group">
          <label for="clean_habit" style="font-weight: bold;">愛乾淨程度：</label>
          <select id="clean_habit" v-model.number="user_data.Clean" required>
            <option value="1">不愛乾淨</option>
            <option value="2">稍微愛乾淨</option>
            <option value="3">正常愛乾淨</option>
            <option value="4">很愛乾淨</option>
            <option value="5">極度潔癖</option>
          </select>
        </div>
        <div class="form-group">
          <label for="mbti" style="font-weight: bold;">Mbti：</label>
          <div class="address-group">
            <select id="EI" v-model="All_MBTI.EI" required>
              <option value="E">E(外向)</option>
              <option value="I">I(內向)</option>
            </select>
            <select id="SN" v-model="All_MBTI.SN" required>
              <option value="S">S(實際)</option>
              <option value="N">N(直覺)</option>
            </select>
            <select id="FT" v-model="All_MBTI.FT" required>
              <option value="F">F(感覺)</option>
              <option value="T">T(思考)</option>
            </select>
            <select id="PJ" v-model="All_MBTI.PJ" required>
              <option value="P">P(感知)</option>
              <option value="J">J(判斷)</option>
            </select>
          </div>
          <!--<input type="text" id="mbti" v-model="user_data.Mbti" required>-->
        </div>

        <!-- Interests -->
        <div class="form-group interests">
          <label style="font-weight: bold;">興趣：</label>
          <div class="interest-item-container">
            <div class="interest-item" 
              v-for="interest in interests" 
              :key="interest.key"
              :class="{ selected: selectedInterests.includes(interest.key) }"
              @click="toggleInterest(interest.key)">
              {{ interest.label }}
            </div>
          </div>
        </div>
      </div>

      <!-- Additional Fields for Old -->
      <div v-if="user_data.Role === 1">
        <div class="form-group">
          <label for="type" style="font-weight: bold;">房屋類別：</label>
          <select id="type" v-model="house_data.Type" required>
            <option value="透天厝">透天厝</option>
            <option value="公寓">公寓</option>
            <option value="華廈">華廈</option>
            <option value="大樓">大樓</option>
            <option value="帝堡">帝堡</option>
            <option value="別墅">別墅</option>
            <option value="三合院">三合院</option>
          </select>
        </div>
        <div class="form-group">
          <label for="fire" style="font-weight: bold;">是否可開火：</label>
          <select id="fire" v-model="house_data.Fire" required>
            <option :value="1">是</option>
            <option :value="0">否</option>
          </select>
        </div>
        <div class="form-group">
          <label for="canNegotiate" style="font-weight: bold;">是否可議價：</label>
          <select id="canNegotiate" v-model="house_data.Negotiate_Price" required>
            <option :value="1">是</option>
            <option :value="0">否</option>
          </select>
        </div>
        <div class="form-group">
          <label for="size" style="font-weight: bold;">房屋大小：(平方公尺)</label>
          <input type="number" id="size" v-model="house_data.Size" required>
        </div>
        <div class="form-group">
          <label style="font-weight: bold;">地址：</label>
          <div class="address-group">
            <input type="text" id="city" v-model="house_data.City" placeholder="城市" required>
            <input type="text" id="district" v-model="house_data.District" placeholder="行政區" required>
            <input type="text" id="street" v-model="house_data.Street" placeholder="路名" required>
            <input type="number" id="floor" v-model="house_data.Floor" placeholder="樓層" required>
          </div>
        </div>
        <div class="section-boxed">
          <label style="font-weight: bold;">房屋家具：</label>
          <div class="data-item" v-for="(item, index) in house_furn_data.Furniture" :key="index">
            <div class="data-item-content">
              <div class="furniture-input-container">
                <input type="text" v-model="item.name" required>
              </div>
              <div class="delete-button" @click="removeFurniture(index)">&times;</div>
            </div>
          </div>
          <div class="add-trait-block" @click="addFurniture">
            <span class="add-icon">+ 新增</span>
          </div>
        </div>

        <div class="section-boxed">
          <label style="font-weight: bold;">房屋交通：</label>
          <div class="data-item" v-for="(item, index) in house_traffic_data.Traffic" :key="index">
            <div class="data-item-content">
              <div class="traffic-input-container">
                <input type="text" v-model="item.name" required>
              </div>
              <div class="delete-button" @click="removeTraffic(index)">&times;</div>
            </div>
          </div>
          <div class="add-trait-block" @click="addTraffic">
            <span class="add-icon">+ 新增</span>
          </div>
        </div>

      </div>

      <div class="btn-group">
        <button type="submit" class="btn-submit">確認</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const All_MBTI = ref({
  EI:'',
  SN:'',
  FT:'',
  PJ:''
})

const user_data = ref({
  Name: '',
  Role: 0,
  Sleep_Time: 0,
  Drink: 6,
  Smoke: 6,
  Clean: 0,
  Mbti: '',
  Shopping: 0,
  Movie: 0,
  Travel: 0,
  Music: 0,
  Read: 0,
  Game: 0,
  PE: 0,
  Science: 0,
  Food: 0
});

const house_data = ref({
  People_ID: 0,
  Size: 0,
  Fire: '',
  Negotiate_Price: '',
  City: '',
  District: '',
  Street: '',
  Floor: '',
  Type: ''
});

const house_furn_data = ref({
  House_ID: 0,
  Furniture: []
});

const house_traffic_data = ref({
  House_ID: 0,
  Traffic: []
});

const interests = [
  { key: 'Shopping', label: '購物' },
  { key: 'Movie', label: '電影' },
  { key: 'Travel', label: '旅行' },
  { key: 'Music', label: '音樂' },
  { key: 'Read', label: '閱讀' },
  { key: 'Game', label: '遊戲' },
  { key: 'PE', label: '運動' },
  { key: 'Science', label: '科學' },
  { key: 'Food', label: '食物' }
];

const selectedInterests = ref([]);

function updateInterests() {
  interests.forEach(interest => {
    user_data.value[interest.key] = selectedInterests.value.includes(interest.key) ? 1 : 0;
  });
}

function toggleInterest(interestKey) {
  const index = selectedInterests.value.indexOf(interestKey);
  if (index === -1) {
    selectedInterests.value.push(interestKey);
  } else {
    selectedInterests.value.splice(index, 1);
  }
  updateInterests();
}

import { useRouter } from 'vue-router';

const router = useRouter();

async function submitForm() {
  
  try {
    user_data.value.Mbti = All_MBTI.value.EI + All_MBTI.value.SN + All_MBTI.value.FT + All_MBTI.value.PJ;

    const userResponse = await axios.post('http://localhost:7877/post_user_basic_info', user_data.value);
    console.log(userResponse.data);
    const People_ID = userResponse.data.People_ID;
    
    if (user_data.value.Role === 1) {
      const houseResponse = await axios.post('http://localhost:7877/post_house_info', {
        ...house_data.value,
        People_ID: People_ID 
      });
      const House_ID = houseResponse.data.House_ID;
      const furnitureResponse = await axios.post('http://localhost:7877/post_house_furniture_info', {
        ...house_furn_data.value,
        House_ID: House_ID,
        Furniture: house_furn_data.value.Furniture.map(f => f.name) 
      });
      console.log(furnitureResponse.data);
      const trafficResponse = await axios.post('http://localhost:7877/post_house_traffic_info', {
        ...house_traffic_data.value,
        House_ID: House_ID,
        Traffic: house_traffic_data.value.Traffic.map(t => t.name) 
      });
      console.log(trafficResponse.data);
      router.push({ path: '/homeold', query: { People_ID } });
    } else {
      router.push({ path: '/homeyoung', query: { People_ID } });
    }
  } catch (error) {
    console.error('Error submitting form:', error);
  }
}

function addFurniture() {
  house_furn_data.value.Furniture.push({ name: '' });
}

function removeFurniture(index) {
  house_furn_data.value.Furniture.splice(index, 1);
}

function addTraffic() {
  house_traffic_data.value.Traffic.push({ name: '' });
}

function removeTraffic(index) {
  house_traffic_data.value.Traffic.splice(index, 1);
}
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.form-group {
  margin-bottom: 20px;
}

.role-options {
  display: flex;
  gap: 20px;
}

.label {
  font-weight: bold;
}

input[type="text"],
input[type="number"],
input[type="email"],
input[type="radio"],
select {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 2px solid #333;
  font-size: 16px;
  box-sizing: border-box;
  margin-top: 5px;
}

.btn-submit {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-submit:hover {
  background-color: #45a049;
}

.btn-group {
  text-align: center;
  margin-top: 20px;
}

.add-icon {
  font-size: 16px;
  font-weight: bold;
}

.interests {
  display: flex;
  flex-direction: column; 
  align-items: center; 
}

.interest-item-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center; 
}

.interest-item {
  padding: 10px 20px;
  border: 2px solid #333;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  background-color: #c2d4dc;
}

.interest-item.selected {
  background-color: #779aa8;
  color: white;
}

.data-item-content {
  position: relative;
}

.furniture-input-container,
.traffic-input-container {
  display: flex;
  align-items: center;
}

.delete-button {
  padding: 4px 8px;
  border-radius: 50%;
  background-color: #f44336;
  color: white;
  cursor: pointer;
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
}

.add-trait-block {
  cursor: pointer;
  display: inline-block;
  width: calc(100% - 32px);
  padding: 8px 16px;
  background-color: #f0f0f0;
  border-radius: 5px;
  margin-bottom: 10px;
}

.add-trait-block:hover {
  background-color: #e0e0e0;
}

.section-boxed {
  border: 1px solid #ccc;
  padding: 10px;
  margin-top: 20px;
}

.address-group {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.section-boxed label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

</style>
