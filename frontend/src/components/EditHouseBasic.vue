<template>
    <div class="edit-overlay">
      <div class="edit-modal">
        <h2>更改房屋基本資料</h2>
        <form @submit.prevent="saveHouseData">
          <!-- House Basic Info Section -->
          <div class="form-group">
            <label for="size">房屋大小：</label>
            <input type="number" id="size" v-model="editedHouseData.size" required>
          </div>
          <div class="form-group">
            <label for="fire">是否可開火：</label>
            <select id="fire" v-model="editedHouseData.fire" required>
              <option value="是">是</option>
              <option value="否">否</option>
            </select>
          </div>
          <div class="form-group">
            <label for="canNegotiate">是否可議價：</label>
            <select id="canNegotiate" v-model="editedHouseData.canNegotiate" required>
              <option value="是">是</option>
              <option value="否">否</option>
            </select>
          </div>
          <div class="form-group">
            <label for="address">地址：</label>
            <input type="text" id="address" v-model="editedHouseData.address" required>
          </div>
          <div class="form-group">
            <label for="floor">樓層：</label>
            <input type="number" id="floor" v-model="editedHouseData.floor" required>
          </div>
          <div class="form-group">
            <label for="houseType">房屋類別：</label>
            <input type="text" id="houseType" v-model="editedHouseData.houseType" required>
          </div>
  
          <div class="btn-group">
            <button type="submit" class="btn-submit">保存</button>
            <button type="button" class="btn-cancel" @click="cancel()">取消</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  // TODO: Complete the unfinished functions"saveHouseData" outlined in ticket [GP103].
  import { ref } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  
  const editedHouseData = ref({
    size: 0,
    fire: '',
    canNegotiate: '',
    address: '',
    floor: 0,
    houseType: '',
  });
  
  const router = useRouter(); 
  const route = useRoute();
  
  function cancel() {
    const from = route.query.from || '/'; 
    router.push(from);
  }
  

  </script>
  
  <style scoped>
  .edit-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .edit-modal {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .form-group input,
  .form-group select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .btn-group {
    text-align: right;
  }
  
  .btn-submit,
  .btn-cancel {
    padding: 8px 16px;
    margin-left: 10px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-submit {
    background-color: #4CAF50;
    color: white;
    border: none;
  }
  
  .btn-submit:hover {
    background-color: #45a049;
  }
  
  .btn-cancel {
    background-color: #f44336;
    color: white;
    border: none;
  }
  
  .btn-cancel:hover {
    background-color: #da190b;
  }
  </style>
  