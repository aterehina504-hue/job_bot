from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, BigInteger
from sqlalchemy.sql import func

from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)

    job_type = Column(String(50))
    salary = Column(String(100))

    short_description = Column(Text)
    full_description = Column(Text)

    contact = Column(String(255))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserBalance(Base):
    __tablename__ = "user_balances"

    user_id = Column(BigInteger, primary_key=True)
    credits = Column(Integer, default=0)
