from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.common.core.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    unique_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="company")
