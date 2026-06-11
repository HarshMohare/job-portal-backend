from fastapi import APIRouter, Depends, HTTPException
from .. import models, schema
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_recruiter


router = APIRouter(
    prefix='/recruiter',
    tags=['Recruiter']
)


# ALL APPLICATIONS FOR ONE COMPANY
@router.get('/{recruiter_id}/applicants', response_model=list[schema.ApplyResponse])
def get_applicants(
    recruiter_id: int,
    db: Session = Depends(get_db),
    current_recruiter=Depends(get_current_recruiter)
):
    if current_recruiter.id != recruiter_id:
        raise HTTPException(status_code=403, detail="Access denied")

    result = db.query(models.Apply, models.Candidates, models.Jobs)\
               .join(models.Candidates, models.Candidates.id == models.Apply.candidate_id)\
               .join(models.Jobs, models.Jobs.id == models.Apply.job_id)\
               .filter(models.Jobs.recruiter_id == recruiter_id)\
               .all()

    if not result:
        raise HTTPException(status_code=404, detail="No applicants found")

    return [
        schema.ApplyResponse(
            id=apply.id,
            candidate=candidate,
            job=job
        )
        for apply, candidate, job in result
    ]


# ADD NEW JOBS
@router.post('/add_jobs', response_model=schema.JobResponse)
def post_jobs(
    job_data: schema.AddJobs,
    db: Session = Depends(get_db),
    current_recruiter=Depends(get_current_recruiter)
):
    if current_recruiter.id != job_data.recruiter_id:
        raise HTTPException(status_code=403, detail="You can only post jobs for yourself")

    new_job = models.Jobs(**job_data.model_dump())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


# DELETE JOBS
@router.delete('/delete_job/{job_id}')
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_recruiter=Depends(get_current_recruiter)
):
    job = db.query(models.Jobs).filter(models.Jobs.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.recruiter_id != current_recruiter.id:
        raise HTTPException(status_code=403, detail="You can only delete your own jobs")

    db.delete(job)
    db.commit()

    return {"message": f"Job {job_id} deleted successfully"}