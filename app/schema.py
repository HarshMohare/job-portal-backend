from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic import ConfigDict


# JOBS 
class AddJobs(BaseModel):
    company_name: str = Field(min_length=2, max_length=100)
    job_title: str = Field(min_length=2, max_length=100)
    job_opening: int = Field(gt=0)
    stipend: int = Field(ge=0)
    recruiter_id: int

# JOB RESPONSE
class JobResponse(AddJobs):
    id: int
    model_config = ConfigDict(from_attributes=True)


# CANDIDATES 
class CandidateResponse(BaseModel):
    candidate_fname: str
    candidate_lname: str
    candidate_email: EmailStr
    model_config = ConfigDict(from_attributes=True)


# APPLY 
class AddJobApply(BaseModel):
    candidate_id: int
    job_id: int

class ApplyResponse(BaseModel):
    id: int
    candidate: CandidateResponse
    job: JobResponse
    model_config = ConfigDict(from_attributes=True)


# REGISTRATION BY CANDIDATE
class NewCandidate(BaseModel):
    candidate_fname: str = Field(min_length=2, max_length=50)
    candidate_lname: str = Field(min_length=2, max_length=50)
    candidate_email: EmailStr
    password: str = Field(min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

# CANDIDATE REGISTRATION RESPONSE
class NewCandidateResponse(BaseModel):
    id: int
    candidate_fname: str
    candidate_lname: str
    candidate_email: EmailStr
    model_config = ConfigDict(from_attributes=True)

# REGISTRATION BY RECRUITER
class NewRecruiter(BaseModel):
    recruiters_company_name: str = Field(min_length=2, max_length=100)
    recruiters_email: EmailStr
    password: str = Field(min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

# RECRUITER REGISTRATION RESPONSE
class NewRecruiterResponse(BaseModel):
    id: int
    recruiters_company_name: str
    recruiters_email: EmailStr
    model_config = ConfigDict(from_attributes=True)


# LOGIN 
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# TOKEN 
class Token(BaseModel):
    access_token: str
    token_type: str