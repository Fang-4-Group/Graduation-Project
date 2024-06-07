<template>
  <div class="container">
    <h1>首次登錄</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label style="margin-right: 10px; font-weight: bold;">你是：</label>
        <div style="display: inline-block;">
          <input type="radio" id="young" value="young" v-model="userData.type">
          <label for="young" style="margin-right: 10px;">年輕人</label>
        </div>
        <div style="display: inline-block;">
          <input type="radio" id="old" value="old" v-model="userData.type">
          <label for="old">老人</label>
        </div>
      </div>

      <!-- Additional fields for both young and old -->
      <div>
        <div class="form-group">
          <label for="sleepTime" style="font-weight: bold;">睡覺時間：</label>
          <input type="number" id="sleepTime" v-model="userData.sleepTime" required>
        </div>
        <div class="form-group">
          <label for="drink_or_smoke" style="font-weight: bold;">菸酒程度：</label>
          <input type="number" id="drink_or_smoke" v-model="userData.drink_or_smoke" required>
        </div>
        <div class="form-group">
          <label for="clean_habit" style="font-weight: bold;">愛乾淨程度：</label>
          <input type="number" id="clean_habit" v-model="userData.clean_habit" required>
        </div>
        <div class="form-group">
          <label for="characters" style="font-weight: bold;">個人特質：</label>
          <div v-for="(trait, index) in userData.characters" :key="index">
            <div class="trait-item">
              <input type="text" v-model="userData.characters[index]" required>
              <span class="delete-button" @click="removeTrait(index)">&times;</span>
            </div>
          </div>
          <div class="add-trait-block" @click="addTrait">
            <span class="add-icon">+ 新增</span>
          </div>
        </div>
        <div class="form-group">
          <label for="interests" style="font-weight: bold;">興趣：</label>
          <div v-for="(interest, index) in userData.interests" :key="index">
            <div class="interest-item">
              <input type="text" v-model="userData.interests[index]" required>
              <span class="delete-button" @click="removeInterest(index)">&times;</span>
            </div>
          </div>
          <div class="add-interest-block" @click="addInterest">
            <span class="add-icon">+ 新增</span>
          </div>
        </div>
      </div>

      <!-- Additional fields for old -->
      <div v-if="userData.type === 'old'">
        <div class="form-group">
          <label for="size" style="font-weight: bold;">房屋大小：</label>
          <input type="number" id="size" v-model="userData.size" required>
        </div>
        <div class="form-group">
          <label for="fire" style="font-weight: bold;">是否可開火：</label>
          <input type="text" id="fire" v-model="userData.fire" required>
        </div>
        <div class="form-group">
          <label for="canNegotiate" style="font-weight: bold;">是否可議價：</label>
          <input type="text" id="canNegotiate" v-model="userData.canNegotiate" required>
        </div>
        <div class="form-group">
          <label for="address" style="font-weight: bold;">地址：</label>
          <input type="text" id="address" v-model="userData.address" required>
        </div>
        <div class="form-group">
          <label for="floor" style="font-weight: bold;">樓層：</label>
          <input type="number" id="floor" v-model="userData.floor" required>
        </div>
        <div class="form-group">
          <label for="houseType" style="font-weight: bold;">房屋類別：</label>
          <input type="text" id="houseType" v-model="userData.houseType" required>
        </div>
      </div>

      <div class="btn-group">
        <button type="submit" class="btn-submit">確認</button>
      </div>
    </form>
  </div>
</template>

<script setup>
 // TODO: Complete the unfinished functions"submitForm" outlined in ticket [GP103].
import { ref } from 'vue';

const userData = ref({
  name: '',
  email: '',
  type: '',
  sleepTime: 0,
  drink_or_smoke: 0,
  clean_habit: 0,
  characters: [''],
  interests: [''],
  size: 0,
  fire: '',
  canNegotiate: '',
  address: '',
  floor: 0,
  houseType: ''
});

function addTrait() {
  userData.value.characters.push('');
}

function removeTrait(index) {
  userData.value.characters.splice(index, 1);
}

function addInterest() {
  userData.value.interests.push('');
}

function removeInterest(index) {
  userData.value.interests.splice(index, 1);
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
</style>
