<template>
  <el-card class="box-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <h2>開始您的 AI 履歷健檢</h2>
      </div>
    </template>

    <div v-if="!analysisResult && !isLoading" class="upload-area">
      <el-upload
        class="upload-demo"
        drag
        action="#"
        :auto-upload="false"
        :on-change="handleFileChange"
        accept="application/pdf"
        :limit="1"
        :show-file-list="false"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">將 PDF 檔案拖曳至此，或 <em>點擊選擇檔案</em></div>
        <template #tip>
          <div class="el-upload__tip text-center">請上傳 PDF 格式的履歷檔案</div>
        </template>
      </el-upload>

      <div v-if="selectedFile" class="action-btn text-center mt-4">
        <p class="mb-3">
          已選擇：<strong>{{ selectedFile.name }}</strong>
        </p>
        <el-button type="primary" size="large" @click="submitResume"> 開始 AI 健檢 </el-button>
      </div>
    </div>

    <div
      v-if="isLoading"
      class="loading-area"
      v-loading="isLoading"
      element-loading-text="🚀 AI 面試官正在仔細閱讀您的履歷，請稍候..."
    >
      <div style="height: 200px"></div>
    </div>

    <div v-if="analysisResult" class="result-area">
      <el-result icon="success" title="健檢報告出爐！">
        <template #extra>
          <h3>
            綜合評分：<span class="score-text">{{ analysisResult.score }}</span> / 100
          </h3>
        </template>
      </el-result>

      <el-divider content-position="left">✨ 主要優點</el-divider>
      <div class="tags-container">
        <el-tag
          v-for="(pro, index) in analysisResult.pros"
          :key="index"
          type="success"
          effect="light"
          class="m-1"
        >
          {{ pro }}
        </el-tag>
      </div>

      <el-divider content-position="left">⚠️ 致命傷與建議</el-divider>
      <div class="tags-container">
        <el-tag
          v-for="(con, index) in analysisResult.cons"
          :key="index"
          type="danger"
          effect="light"
          class="m-1"
        >
          {{ con }}
        </el-tag>
      </div>

      <div class="text-center mt-5">
        <el-button type="primary" plain @click="resetForm">重新上傳一份</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
// 引入 Element Plus 的圖示
import { UploadFilled } from '@element-plus/icons-vue'
import { uploadResume } from "../api";

const selectedFile = ref(null)
const isLoading = ref(false)
const analysisResult = ref(null)

const handleFileChange = (uploadFile) => {
  const file = uploadFile.raw
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file
  } else {
    // 使用 Element Plus 的訊息提示
    ElMessage.error('請上傳 PDF 格式的檔案！')
  }
}

const submitResume = async () => {
  if (!selectedFile.value) return;

  isLoading.value = true;
  
  try {
    // 3. 呼叫真實的後端 API，將檔案送出
    const responseData = await uploadResume(selectedFile.value);
    
    // 4. 將後端回傳的資料放進結果中渲染
    analysisResult.value = responseData;
    
  } catch (error) {
    // 🌟 關鍵判斷：如果錯誤狀態碼是 401，什麼都不做 (攔截器會處理跳轉)
    if (error.response && error.response.status === 401) {
       console.log("Token 過期，交給攔截器處理跳轉...");
       return; // 提早結束，不要執行後面的 alert
    }

    // 如果不是 401 (例如 500 伺服器掛了，或是網路斷線)，才跳出警告
    alert('上傳分析失敗，請檢查後端伺服器是否開啟，或稍後再試。');
  } finally {
    isLoading.value = false;
  }
};

const resetForm = () => {
  selectedFile.value = null
  analysisResult.value = null
}
</script>

<style scoped>
.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #303133;
  text-align: center;
}

.text-center {
  text-align: center;
}

.mt-4 {
  margin-top: 1rem;
}
.mt-5 {
  margin-top: 2rem;
}
.mb-3 {
  margin-bottom: 1rem;
}
.m-1 {
  margin: 0.5rem;
}

.score-text {
  font-size: 2rem;
  color: #67c23a;
  font-weight: bold;
}

.tags-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
