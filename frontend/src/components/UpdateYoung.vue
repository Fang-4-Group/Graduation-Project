<template>
    <div class="container">
      <h1>更改資料(青)</h1>
      <form @submit.prevent="submitForm">
        <!-- Common Fields -->
        <div>
          <div class="form-group">
            <label for="name" style="font-weight: bold;">姓名：</label>
            <input type="text" id="name" v-model="user_data.Name" required>
          </div>
          <div class="form-group">
            <label for="sleepTime" style="font-weight: bold;">睡覺時間：</label>
            <select id="sleepTime" v-model.number="user_data.Sleep_Time" required>
              <option v-for="(label, value) in sleepTimeLabels" :key="value" :value="Number(value)">
                {{ label }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="drink" style="font-weight: bold;">飲酒程度：</label>
            <select id="drink" v-model.number="user_data.Drink" required>
              <option v-for="(label, value) in drinkLabels" :key="value" :value="Number(value)">
                {{ label }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="smoke" style="font-weight: bold;">抽菸程度：</label>
            <select id="smoke" v-model.number="user_data.Smoke" required>
              <option v-for="(label, value) in smokeLabels" :key="value" :value="Number(value)">
                {{ label }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="clean_habit" style="font-weight: bold;">愛乾淨程度：</label>
            <select id="clean_habit" v-model.number="user_data.Clean" required>
              <option v-for="(label, value) in cleanLabels" :key="value" :value="Number(value)">
                {{ label }}
              </option>
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
  
        <div class="btn-group">
          <button type="submit" class="btn-submit">確認更改</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';
  const BASE_URL = 'http://localhost:7877';
  
  const route = useRoute();
  const People_ID = route.query.People_ID;
  
  const user_data = ref({
    Name: '',
    Sleep_Time: null,
    Drink: null,
    Smoke: null,
    Clean: null,
  });
  
  const All_MBTI = ref({
    EI: '',
    SN: '',
    FT: '',
    PJ: '',
  });
  
  const selectedInterests = ref([]);
  const interests = ref([
    { key: 'Shopping', label: '購物' },
    { key: 'Movie', label: '電影' },
    { key: 'Travel', label: '旅行' },
    { key: 'Music', label: '音樂' },
    { key: 'Read', label: '閱讀' },
    { key: 'Game', label: '遊戲' },
    { key: 'PE', label: '運動' },
    { key: 'Science', label: '科學' },
    { key: 'Food', label: '食物' }
  ]);
  
  const sleepTimeLabels = {
    1: '晚上7:00~9:00',
    2: '晚上9:00~11:00',
    3: '晚上11:00~凌晨1:00',
    4: '凌晨1:00~3:00',
    5: '凌晨3:00以後'
  };
  
  const drinkLabels = {
    0: '從不飲酒',
    1: '很少飲酒',
    2: '偶爾小酌',
    3: '經常飲酒',
    4: '每天飲酒'
  };
  
  const smokeLabels = {
    0: '從不抽菸',
    1: '很少抽菸',
    2: '偶爾抽菸',
    3: '經常抽菸',
    4: '每天抽菸'
  };
  
  const cleanLabels = {
    1: '不愛乾淨',
    2: '稍微愛乾淨',
    3: '正常愛乾淨',
    4: '很愛乾淨',
    5: '極度潔癖'
  };
  
  const fetchUserData = async () => {
    try {
      const responses = await Promise.all([
        axios.get(`${BASE_URL}/get_name/${People_ID}`),
        axios.get(`${BASE_URL}/get_sleep_time/${People_ID}`),
        axios.get(`${BASE_URL}/get_drink/${People_ID}`),
        axios.get(`${BASE_URL}/get_smoke/${People_ID}`),
        axios.get(`${BASE_URL}/get_clean_habit/${People_ID}`),
        axios.get(`${BASE_URL}/get_mbti/${People_ID}`),
        axios.get(`${BASE_URL}/get_interests/${People_ID}`)
      ]);
  
      console.log('API responses:', responses);
  
      user_data.value.Name = typeof responses[0].data === 'string' ? responses[0].data : responses[0].data.name; 
      user_data.value.Sleep_Time = Number(responses[1].data.sleep_time);
      user_data.value.Drink = Number(responses[2].data.drink);
      user_data.value.Smoke = Number(responses[3].data.smoke);
      user_data.value.Clean = Number(responses[4].data.clean_habit);
  
      const mbti = responses[5].data.mbti || '';
      const mbtiArray = mbti.split('');
      if (mbtiArray.length === 4) {
        All_MBTI.value.EI = mbtiArray[0];
        All_MBTI.value.SN = mbtiArray[1];
        All_MBTI.value.FT = mbtiArray[2];
        All_MBTI.value.PJ = mbtiArray[3];
      } else {
        console.error('MBTI data format is incorrect:', mbti);
      }
  
      // Ensure selectedInterests is an array
      selectedInterests.value = Array.isArray(responses[6].data.interests) ? responses[6].data.interests : [];
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };
  
  onMounted(fetchUserData);
  
  const submitForm = async () => {
    // Your form submission logic
    console.log("submit")
  };
  
  const toggleInterest = (interest) => {
    if (selectedInterests.value.includes(interest)) {
      selectedInterests.value = selectedInterests.value.filter((i) => i !== interest);
    } else {
      selectedInterests.value.push(interest);
    }
  };
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
    margin-top: 5px;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ccc;
    box-sizing: border-box;
  }
  
  .address-group {
    display: flex;
    gap: 10px;
  }
  
  .interests {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .interest-item-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .interest-item {
    padding: 10px 15px;
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 5px;
    cursor: pointer;
    user-select: none;
  }
  
  .interest-item.selected {
    background-color: #007bff;
    color: white;
    border-color: #007bff;
  }
  
  .btn-group {
    text-align: right;
  }
  
  .btn-submit {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
  }
  
  .btn-submit:hover {
    background-color: #0056b3;
  }
  </style>
  