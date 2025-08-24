from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    guardian = Column(Boolean, default=False)
    login_id = Column(String(50), nullable=False)

    # 보호자 관계 (자기참조)
    guardian_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # 관계 설정
    protected_users = relationship("User", backref="guardian_user", remote_side=[id])
