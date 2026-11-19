from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    specialization = Column(String)

    patients = relationship("Patient", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    status = Column(String, default="waiting")  # waiting, in_consultation, completed

    doctor = relationship("Doctor", back_populates="patients")