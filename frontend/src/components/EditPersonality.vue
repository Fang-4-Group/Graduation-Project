<template>
    <div class="edit-overlay">
      <div class="edit-modal">
        <h2>新增個人特質</h2>
        <form @submit.prevent="saveUserData">
          <!-- Personality Traits Section -->
          <div class="form-group" v-for="(trait, index) in traits" :key="index">
            <label :for="'trait-' + index">個人特質：</label>
            <input type="text" :id="'trait-' + index" v-model="editedUserData.personalityTraits[index]" required>
          </div>
  
          <!-- Add New Trait Block -->
          <div class="add-trait-block" @click="addNewTrait" @mouseover="hovered = true" @mouseleave="hovered = false">
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
  // TODO: Complete the unfinished functions"saveUserData" outlined in ticket [GP103].
  import { ref } from 'vue';
  import { useRouter , useRoute } from 'vue-router';
  
  const editedUserData = ref({
  
    personalityTraits: [''], 
  });
  
  const traits = ref(editedUserData.value.personalityTraits); 
  const hovered = ref(false); 
  const router = useRouter(); 
  

  
  const route = useRoute();
  
  function cancel() {
    const from = route.query.from || '/'; 
    router.push(from);
  }

  function addNewTrait() {
    traits.value.push(''); 
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
  
  .add-trait-block {
    cursor: pointer;
    display: inline-block;
    padding: 8px 16px;
    background-color: #f0f0f0;
    border-radius: 4px;
    margin-bottom: 10px;
  }
  
  .add-trait-block:hover {
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