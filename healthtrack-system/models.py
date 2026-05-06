from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

# This is the "Anchor" that links everything to the database
DBModelBase = declarative_base()

class Patient(DBModelBase):
    __tablename__ = "patients"
    
    # Required Patient Data (Case Study Page 2)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())) # Patient ID (UUID)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False) # Age
    primary_issue = Column(String, nullable=False) # Checkup, Follow-up, etc.
    no_show_probability = Column(Float, nullable=False) # Decimal value

class Appointment(DBModelBase):
    __tablename__ = "appointments"
    
    # Required Appointment Data (Case Study Page 2)
    appointment_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(DateTime, default=datetime.utcnow) # Date
    day_of_week = Column(String) # Monday, Tuesday, etc.
    time_slot = Column(String) # 9:00AM, 10:00AM, etc.
    patient_id = Column(String, ForeignKey("patients.id")) # Borrowed from Patient
    appointment_type = Column(String) # Borrowed from Patient
    scheduled_duration = Column(Integer) # Integer
    actual_duration = Column(Integer) # Integer
    show_up_status = Column(Boolean) # Boolean
    duration_difference = Column(Integer) # Difference