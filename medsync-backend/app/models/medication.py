from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String)
    schedule = Column(String)  # e.g., "1-0-1" or "Every 6 hours"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # We can eventually link this to a User ID
    # user_id = Column(Integer, ForeignKey("users.id"))