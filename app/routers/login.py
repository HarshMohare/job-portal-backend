from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schema
from ..database import get_db
from ..auth import hash_password, verify_password, create_token

router = APIRouter(prefix='/login', tags=['Login'])


# REGISTER CANDIDATE
@router.post('/register_candidate', response_model=schema.NewCandidateResponse)
def register_candidate(data: schema.NewCandidate, db: Session = Depends(get_db)):
    existing = db.query(models.Candidates).filter(
        models.Candidates.candidate_email == data.candidate_email
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    candidate = models.Candidates(
        candidate_fname=data.candidate_fname,
        candidate_lname=data.candidate_lname,
        candidate_email=data.candidate_email,
        password=hash_password(data.password)
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

# REGISTER RECRUITER
@router.post('/register_recruiter', response_model=schema.NewRecruiterResponse)
def register_recruiter(data: schema.NewRecruiter, db: Session = Depends(get_db)):
    existing = db.query(models.Recruiters).filter(
        models.Recruiters.recruiters_email == data.recruiters_email
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    recruiter = models.Recruiters(
        recruiters_company_name=data.recruiters_company_name,
        recruiters_email=data.recruiters_email,
        password=hash_password(data.password)
    )
    db.add(recruiter)
    db.commit()
    db.refresh(recruiter)
    return recruiter


# LOGIN CANDIDATE
@router.post('/candidate', response_model=schema.Token)
def login_candidate(data: schema.LoginRequest, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidates).filter(
        models.Candidates.candidate_email == data.email
    ).first()

    if not candidate or not verify_password(data.password, candidate.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token({"sub": candidate.candidate_email, "role": "candidate"})
    return {"access_token": token, "token_type": "bearer"}

# LOGIN RECRUITER
@router.post('/recruiter', response_model=schema.Token)
def login_recruiter(data: schema.LoginRequest, db: Session = Depends(get_db)):
    recruiter = db.query(models.Recruiters).filter(
        models.Recruiters.recruiters_email == data.email
    ).first()

    if not recruiter or not verify_password(data.password, recruiter.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token({"sub": recruiter.recruiters_email, "role": "recruiter"})
    return {"access_token": token, "token_type": "bearer"}