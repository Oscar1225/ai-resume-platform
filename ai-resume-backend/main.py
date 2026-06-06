from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # 👈 新增這行
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import jwt
import datetime
import pdfplumber
import io
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
# 引入資料庫設定 (確保您的後端資料夾內已經有寫好的 database.py)
from database import UserDB, get_db
load_dotenv()
app = FastAPI(title="AI 職涯媒合 API")

# --- 1. CORS 跨網域設定 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://ai-resume-platform-iota.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Gemini AI 設定 ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("找不到 GEMINI_API_KEY，請確認 .env 檔案是否設定正確！")
genai.configure(api_key=GEMINI_API_KEY)

# --- 3. 密碼加密與 JWT 設定 ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my_super_secret_key")
ALGORITHM = "HS256"
security = HTTPBearer()
# --- 4. 定義前端傳來的資料格式 (Pydantic Models) ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "user" # 預設為一般求職者

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ==========================================
#               API 路由區塊
# ==========================================
# 🛡️ 這是新增的：JWT 驗證警衛函數
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials # 取得純 Token 字串
    try:
        # 解碼 JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="無效的憑證")
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="登入已過期，請重新登入！")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="無效的憑證，拒絕存取！")
    
    # 去資料庫尋找該名使用者
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="找不到此使用者")
        
    return user

# --- 註冊 API ---
@app.post("/v1/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 1. 檢查信箱是否已被註冊
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="此 Email 已經註冊過了！")
    
    # 2. 將密碼加密
    hashed_password = pwd_context.hash(user.password)
    
    # 3. 存入資料庫
    new_user = UserDB(
        email=user.email, 
        password_hash=hashed_password, 
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "註冊成功！", "user_id": new_user.id}

# --- 登入 API ---
@app.post("/v1/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # 1. 尋找使用者
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")
    
    # 2. 驗證密碼
    if not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")
    
    # 3. 產生 JWT (包含使用者的 ID, role 與過期時間)
    payload = {
        "sub": str(db_user.id),
        "role": db_user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24) # 24 小時後過期
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "message": "登入成功",
        "access_token": token,
        "role": db_user.role
    }

# --- AI 履歷健檢 API ---
@app.post("/v1/resume/analyze")
async def analyze_resume(resume_file: UploadFile = File(...), current_user: UserDB = Depends(get_current_user)):
    if not resume_file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="請上傳 PDF 格式的檔案")

    try:
        file_content = await resume_file.read()
        
        text_content = ""
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text_content += extracted_text + "\n"
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="無法擷取文字，請確保履歷不是純圖片。")

        print("文字擷取成功，正在呼叫 AI 進行分析...")

        # 設定 Gemini 模型與提示詞
        model = genai.GenerativeModel('gemini-3.5-flash')
        
        prompt = f"""
        你是一位在科技業有 10 年經驗的資深人資(HR)與技術主管。
        請閱讀以下應徵者的履歷內容，並給予嚴格但具建設性的健檢建議。
        
        【重要輸出規則】：
        你必須且只能回傳一個合法的 JSON 格式字串，不能包含任何 Markdown 標記 (如 ```json) 或其他說明文字。
        JSON 格式必須包含以下三個欄位：
        1. "score": 綜合評分 (0-100的整數)
        2. "pros": 陣列，包含 3 個具體的優點 (字串)
        3. "cons": 陣列，包含 3 個致命傷或具體的改進建議 (字串)

        以下是履歷內容：
        {text_content}
        """

        response = model.generate_content(prompt)
        
        # 清理 AI 的回覆並轉為 Python 字典
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        result_json = json.loads(raw_text.strip())
        print("AI 分析完成！")
        
        return result_json

    except Exception as e:
        print(f"解析或 AI 呼叫錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail="伺服器處理或 AI 分析失敗，請稍後再試。")