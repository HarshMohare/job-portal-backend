from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship



# TABLE 1 : CANDIDATES
class Candidates(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    candidate_fname = Column(String, nullable=False)
    candidate_lname = Column(String, nullable=False)
    candidate_email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    applications = relationship("Apply", back_populates="candidate")

# TABLE 2 : RECRUITERS
class Recruiters(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, index=True)
    recruiters_company_name = Column(String, nullable=False)
    recruiters_email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) 

    jobs = relationship("Jobs", back_populates="recruiter")

# TABLE 3 : JOBS
class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    company_name = Column(String, unique=True, nullable=False)
    job_title = Column(String, nullable=False)
    job_opening = Column(Integer, nullable=False)
    stipend = Column(Integer, nullable=False)

    recruiter_id = Column(Integer, ForeignKey("recruiters.id"), nullable=False)

    recruiter = relationship("Recruiters", back_populates="jobs")  
    applications = relationship("Apply", back_populates="job")

# TABLE 1 : APPLY
class Apply(Base):
    __tablename__ = "jobs_apply"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    candidate = relationship("Candidates", back_populates="applications")
    job = relationship("Jobs", back_populates="applications")