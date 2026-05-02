from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base 

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String)
    schedule = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)