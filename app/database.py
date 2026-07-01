from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ الصق الرابط هنا بعد التعديل
SQLALCHEMY_DATABASE_URL = "postgresql://postgres.wdcfyhsnjbcidpzhlvno:QWER-1234asdfg@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres?sslmode=require"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()