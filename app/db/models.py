from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func

from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)

    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)

    job_type = Column(String(50))          # full-time / part-time / season
    salary = Column(String(100))            # "от 1800 €"

    short_description = Column(Text)        # для канала
    full_description = Column(Text)         # для "Подробнее"

    contact = Column(String(255))            # WhatsApp / Email

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

from sqlalchemy import BigInteger


class UserPayment(Base):
    __tablename__ = "user_payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    job_id = Column(Integer, nullable=False)

    is_used = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
