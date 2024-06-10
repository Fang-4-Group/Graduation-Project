<template>
  <div class="container">
    <h1>首次登錄</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label style="margin-right: 10px; font-weight: bold;">你是：</label>
        <div style="display: inline-block;">
          <input type="radio" id="young" :value="0" v-model="user_data.Role">
          <label for="young" style="margin-right: 10px;">年輕人</label>
        </div>
        <div style="display: inline-block;">
          <input type="radio" id="old" :value="1" v-model="user_data.Role">
          <label for="old">老人</label>
        </div>
      </div>

      <!-- Additional fields for both young and old -->
      <div>
        <div class="form-group">
          <label for="name" style="font-weight: bold;">姓名：</label>
          <input type="text" id="name" v-model="user_data.Name" required>
        </div>
        <div class="form-group">
          <label for="sleepTime" style="font-weight: bold;">睡覺時間：</label>
          <input type="number" id="sleepTime" v-model="user_data.Sleep_Time" required>
        </div>
        <div class="form-group">
          <label for="drink" style="font-weight: bold;">飲酒程度：</label>
          <input type="number" id="drink" v-model="user_data.Drink" required>
        </div>
        <div class="form-group">
          <label for="smoke" style="font-weight: bold;">抽菸程度：</label>
          <input type="number" id="smoke" v-model="user_data.Smoke" required>
        </div>
        <div class="form-group">
          <label for="clean_habit" style="font-weight: bold;">愛乾淨程度：</label>
          <input type="number" id="clean_habit" v-model="user_data.Clean" required>
        </div>
        <div class="form-group">
          <label for="mbti" style="font-weight: bold;">Mbti：</label>
          <input type="text" id="mbti" v-model="user_data.Mbti" required>
        </div>
        
        <!-- Interest selection -->
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

      <!-- Additional fields for old -->
       
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
          <label for="size" style="font-weight: bold;">房屋大小：</label>
          <input type="number" id="size" v-model="house_data.Size" required>
        </div>
        
        <div class="form-group">
          <label for="address" style="font-weight: bold;">地址(城市)：</label>
          <input type="text" id="city" v-model="house_data.City" required>
        </div>
        <div class="form-group">
          <label for="district" style="font-weight: bold;">地址(行政區)：</label>
          <input type="text" id="district" v-model="house_data.District" required>
        </div>
        <div class="form-group">
          <label for="street" style="font-weight: bold;">地址(路名)：</label>
          <input type="text" id="street" v-model="house_data.Street" required>
        </div>
        <div class="form-group">
          <label for="floor" style="font-weight: bold;">樓層：</label>
          <input type="number" id="floor" v-model="house_data.Floor" required>
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

const user_data = ref({
  Name: '',
  Role: 0,
  Sleep_Time: 0,
  Drink: 0,
  Smoke: 0,
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
    const userResponse = await axios.post('http://localhost:7877/post_user_basic_info', user_data.value);
    console.log(userResponse.data);
    
    // 获取用户的 People_ID
    const People_ID = userResponse.data.People_ID;

    // 如果用户是老年人，提交房屋信息
    if (user_data.value.Role === 1) {
      // 将用户的 People_ID 关联到房屋信息中
      const houseResponse = await axios.post('http://localhost:7877/post_house_info', {
        ...house_data.value,
        People_ID: People_ID // 使用相同的 People_ID
      });
      console.log(houseResponse.data);
      router.push({ path: '/homeold', query: { People_ID } });
    } else {
      router.push({ path: '/homeyoung', query: { People_ID } });
    }
  } catch (error) {
    console.error('Error submitting form:', error);
  }
}

</script>

<style scoped>
.selected {
  background-color: #4CAF50;
  color: white;
}

.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.form-group {
  margin-bottom: 20px;
}

.label {
  font-weight: bold;
}

input[type="text"],
input[type="number"],
input[type="email"],
input[type="radio"] {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 2px solid #333; /* 加粗的邊框 */
  font-size: 16px;
  box-sizing: border-box;
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
}

.add-button,
.delete-button {
  padding: 6px 12px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  line-height: 0.8;
  background-color: #f44336;
  color: white;
}

.add-button {
  background-color: #4CAF50;
}

.add-button:hover,
.delete-button:hover {
  box-shadow: 0px 4px 8px rgba(0, 0, 255, 0.2); /* 水平偏移、垂直偏移、模糊程度、顏色 */
}

.trait-item,
.interest-item {
  position: relative;
}

.delete-button {
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
}

.add-trait-block,
.add-interest-block {
  cursor: pointer;
  display: inline-block;
  width: calc(100% - 32px); /* 將寬度設置為100%，但減去左右邊距的總寬度 */
  padding: 8px 16px;
  background-color: #f0f0f0;
  border-radius: 5px;
  margin-bottom: 10px;
}

.add-trait-block:hover,
.add-interest-block:hover {
  background-color: #e0e0e0;
}

.add-icon {
  font-size: 16px;
  font-weight: bold;
}

.interests {
  display: flex;
  flex-direction: column; /* 设置为列方向 */
  align-items: center; /* 水平居中对齐 */
}

.interest-item-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center; /* 水平居中对齐 */
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
</style>
