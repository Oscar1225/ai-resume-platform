from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
# ⚠️ 請替換成您本地端 MySQL 的 帳號 與 密碼
# 格式：mysql+pymysql://帳號:密碼@伺服器位址:埠號/資料庫名稱
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("找不到 DATABASE_URL，請確認 .env 檔案是否設定正確！")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 定義 Users 資料表結構
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False) # user, company, admin

# 自動在 MySQL 中建立資料表 (如果還不存在的話)
Base.metadata.create_all(bind=engine)

# 取得資料庫連線的依賴函數
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()