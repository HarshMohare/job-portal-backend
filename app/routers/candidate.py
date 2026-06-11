from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException
from .. import models, schema
from ..models import Apply, Jobs, Candidates
from ..auth import get_current_candidate


router = APIRouter(
    prefix='/jobs',
    tags=['Jobs']
)


# SHOW ALL JOBS
@router.get('/', response_model=list[schema.JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Jobs).all()
    return jobs


# APPLY FOR JOBS
@router.post("/apply", response_model=schema.ApplyResponse)
def apply_for_jobs(
    apply_data: schema.AddJobApply,
    db: Session = Depends(get_db),
    current_candidate=Depends(get_current_candidate)
):
    if current_candidate.id != apply_data.candidate_id:
        raise HTTPException(status_code=403, detail="Access denied")

    
    candidate = db.query(models.Candidates).filter(
        models.Candidates.id == apply_data.candidate_id
    ).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    job = db.query(models.Jobs).filter(
        models.Jobs.id == apply_data.job_id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    already_applied = db.query(models.Apply).filter(
        models.Apply.candidate_id == apply_data.candidate_id,
        models.Apply.job_id == apply_data.job_id
    ).first()

    if already_applied:
        raise HTTPException(status_code=400, detail="Already applied for this job")

    application = models.Apply(**apply_data.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)

    return schema.ApplyResponse(
    id=application.id,
    candidate=candidate,
    job=job
)


# CANDIDATE ALL APPLIED JOBSSS
@router.get('/applied_jobs', response_model=list[schema.ApplyResponse])
def applied_by_candidate(
    db: Session = Depends(get_db),
    current_candidate=Depends(get_current_candidate)
):
    result = db.query(Apply, Candidates, Jobs)\
               .join(Candidates, Candidates.id == Apply.candidate_id)\
               .join(Jobs, Jobs.id == Apply.job_id)\
               .filter(Apply.candidate_id == current_candidate.id)\
               .all()

    if not result:
        raise HTTPException(status_code=404, detail="No applications found")

    return [
        schema.ApplyResponse(id=apply.id, candidate=candidate, job=job)
        for apply, candidate, job in result
    ]