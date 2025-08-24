from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 연결 정보 (본인 환경에 맞게 수정)
DATABASE_URL = "mysql+pymysql://root:qlalf5652@localhost:3306/hackerthon"

# 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

# 세션 로컬
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 (모델들이 상속받음)
Base = declarative_base()
