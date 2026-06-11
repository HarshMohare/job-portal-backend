from datetime import datetime, timedelta , timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from . import models
from .database import get_db
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TOKENS FOR CANDIDATE AND RECRUITER
candidate_bearer = HTTPBearer()
recruiter_bearer = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# GET CURRENT LOGGED-IN CANDIDATE
def get_current_candidate(
    credentials: HTTPAuthorizationCredentials = Depends(candidate_bearer),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role != "candidate":
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    candidate = db.query(models.Candidates).filter(
        models.Candidates.candidate_email == email
    ).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


# GET CURRENT LOGGED-IN RECRUITER
def get_current_recruiter(
    credentials: HTTPAuthorizationCredentials = Depends(recruiter_bearer),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role != "recruiter":
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    recruiter = db.query(models.Recruiters).filter(
        models.Recruiters.recruiters_email == email
    ).first()

    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    return recruiter