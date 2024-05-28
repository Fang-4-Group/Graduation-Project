<template>
    <div class="edit-overlay">
      <div class="edit-modal">
        <h2>新增交通</h2>
        <form @submit.prevent="saveTransportData">
          <!-- Transportation Modes Section -->
          <div class="form-group" v-for="(mode, index) in transportModes" :key="index">
            <label :for="'transport-' + index">交通方式：</label>
            <input type="text" :id="'transport-' + index" v-model="editedUserData.transportation[index]" required>
          </div>
  
          <!-- Add New Transportation Mode Block -->
          <div class="add-transport-block" @click="addNewTransportMode" @mouseover="hovered = true" @mouseleave="hovered = false">
            <span class="add-icon">+ 新增</span>
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
  import { ref } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  
  const editedUserData = ref({
    transportation: [''], 
  });
  
  const transportModes = ref(editedUserData.value.transportation); // 将 transportModes 设置为响应式数据
  const hovered = ref(false); // 控制 hover 效果
  const router = useRouter(); // 获取 router 实例
  const route = useRoute(); // 获取当前 route 实例
  
  function cancel() {
    const from = route.query.from || '/'; // 如果没有传递参数，默认回到首页
    router.push(from);
  }
  
  function addNewTransportMode() {
    transportModes.value.push(''); // 添加一个空字符串，新的输入框会出现
  }
  
  </script>
  
  <style scoped>
  /* Edit Modal Styles */
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
  
  .form-group input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .add-transport-block {
    cursor: pointer;
    display: inline-block;
    padding: 8px 16px;
    background-color: #f0f0f0;
    border-radius: 4px;
    margin-bottom: 10px;
  }
  
  .add-transport-block:hover {
    background-color: #e0e0e0;
  }
  
  .add-icon {
    font-size: 16px;
    font-weight: bold;
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
  