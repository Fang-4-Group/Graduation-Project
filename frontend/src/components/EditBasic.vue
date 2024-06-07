<template>
    <div class="edit-overlay">
      <div class="edit-modal">
        <h2>更改基本資料</h2>
        <form @submit.prevent="saveUserData">
          <!-- Basic Info Section -->
          <div class="form-group">
            <label for="sleepTime">睡覺時間：</label>
            <input type="number" id="sleepTime" v-model="editedUserData.basicInfo.sleepTime" required>
          </div>
          <div class="form-group">
            <label for="alcoholLevel">菸酒程度：</label>
            <input type="number" id="alcoholLevel" v-model="editedUserData.basicInfo.alcoholLevel" required>
          </div>
          <div class="form-group">
            <label for="cleanlinessLevel">愛乾淨程度：</label>
            <input type="number" id="cleanlinessLevel" v-model="editedUserData.basicInfo.cleanlinessLevel" required>
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
  // TODO: Complete the unfinished functions"saveUserData" outlined in ticket [GP103].
  import { ref } from 'vue';
  import { useRouter ,useRoute } from 'vue-router';
  
  const editedUserData = ref({
    basicInfo: {
      sleepTime: 0,
      alcoholLevel: 0,
      cleanlinessLevel: 0,
    },
   
  });
  
  const router = useRouter(); // 獲取 router 實例
  const route = useRoute();
  
  function cancel() {
    const from = route.query.from || '/'; // 如果没有传递参数，默认回到首页
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

.form-group input {
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
  