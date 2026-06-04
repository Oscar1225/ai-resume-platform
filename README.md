# 🚀 AI 職涯平台 (AI Resume Platform)

這是一個基於 AI 技術的現代化全端職涯服務平台，結合了前端單頁應用程式 (SPA) 與高效能後端 API。平台提供 **AI 履歷健檢**、**AI 履歷撰寫**、**AI 職缺媒合** 以及 **AI 模擬面試** 四大核心功能，並具備完整的 JWT 身分驗證機制與響應式網頁設計 (RWD)。

## 🛠️ 技術棧 (Tech Stack)

- **前端 (Frontend):** Vue 3 (Composition API), Pinia (狀態管理), Vue Router (路由導覽守衛), Element Plus (UI 組件庫), Axios (API 請求攔截器)
- **後端 (Backend):** FastAPI (Python 異步網絡框架), SQLAlchemy (ORM), PyJWT (身分驗證), Passlib/Bcrypt (密碼雜湊加密)
- **大語言模型 (LLM):** Google Gemini 3.5 Flash API
- **資料庫 (Database):** MySQL

## 📁 專案架構 (Project Structure)

```text
ai-resume-platform/
├── ai-resume-checker/     # Vue 3 前端專案
├── ai-resume-backend/     # FastAPI 後端專案
└── README.md              # 專案說明文件
🚀 快速開始 (Getting Started)
請按照以下步驟在本地端複製、安裝並執行本專案。

1. 複製專案 (Clone Repository)
打開終端機，執行以下指令將專案複製到本地端：

Bash
git clone [https://github.com/Oscar1225/ai-resume-platform.git](https://github.com/Oscar1225/ai-resume-platform.git)
cd ai-resume-platform
2. 後端環境建置與執行 (Backend Setup)
後端基於 Python FastAPI，需建置虛擬環境並配置本地端 MySQL 資料庫。

Step A: 準備 MySQL 資料庫
打開您的 MySQL 管理工具 (如 XAMPP, MySQL Workbench)，執行以下 SQL 建立空白資料庫：

SQL
CREATE DATABASE ai_resume_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
Step B: 初始化 Python 虛擬環境
進入後端資料夾，建立並啟用虛擬環境：

Bash
cd ai-resume-backend
py -m venv venv

# Windows (PowerShell) 啟用虛擬環境
.\venv\Scripts\Activate.ps1

# macOS / Linux 啟用虛擬環境
source venv/bin/activate
Step C: 安裝依賴套件
在虛擬環境啟用狀態下，安裝所有必要的 Python 套件：

Bash
pip install fastapi uvicorn sqlalchemy pymysql passlib[bcrypt] bcrypt==3.2.2 pyjwt pydantic[email] python-dotenv pdfplumber google-generativeai
Step D: 配置環境變數 (.env)
在 ai-resume-backend/ 資料夾根目錄下建立一個 .env 檔案，並填入您的機密金鑰（此檔案已被納入 .gitignore，不會上傳至 GitHub）：

程式碼片段
GEMINI_API_KEY=您的_GEMINI_API_KEY
JWT_SECRET_KEY=自訂的一串隨機安全密鑰字串
DATABASE_URL=mysql+pymysql://root:您的密碼@localhost:3306/ai_resume_db
Step E: 啟動後端伺服器
Bash
uvicorn main:app --reload
啟動成功後，後端 API 將運行在 http://127.0.0.1:8000。您可瀏覽 http://127.0.0.1:8000/docs 查看自動生成的 Swagger API 文件。

3. 前端環境建置與執行 (Frontend Setup)
前端基於 Node.js 與 Vue Vite 架構。

Step A: 開啟新的終端機視窗並進入前端資料夾
Bash
cd ai-resume-checker
Step B: 安裝 Node 套件依赖
Bash
npm install
Step C: 啟動前端開發伺服器
Bash
npm run dev
啟動成功後，終端機會提供一個本地端網址（通常為 http://localhost:5173/）。打開瀏覽器造訪該網址即可開始使用平台！

🔒 安全防護說明
本專案在推波至 GitHub 前已做好以下商用等級安全防護：

密碼安全性: 使用 bcrypt 進行單向雜湊加鹽加密，資料庫不儲存任何明文密碼。

門禁防護 (JWT): 所有核心 AI 功能 API（如履歷健檢）皆掛載了後端驗證依賴警衛。未帶合法認證 Token 的請求將直接被攔截。

前端防漏: 配置 Axios 攔截器 自動追蹤 localStorage 憑證並補帶 Token，且設有 Vue Router 路由守衛 杜絕未登入使用者硬闖後台。

環境變數分離: 所有的 API Key、資料庫密碼皆抽離至 .env 中，配合頂層 .gitignore 確保敏感數據永不外洩。
