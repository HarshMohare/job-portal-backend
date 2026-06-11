# Job Portal Backend API

A REST API built with FastAPI and PostgreSQL for managing job postings and applications.

## Features

* JWT Authentication
* Candidate & Recruiter Registration/Login
* Role-Based Authorization
* Job Posting and Management
* Job Application System
* View Applied Jobs
* View Applicants
* Password Hashing with Bcrypt
* Pydantic Validation

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT Authentication

## Installation

### Clone the repository

```bash
git clone https://github.com/HarshMohare/job-portal-backend.git
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create `.env` file

```env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run the server

```bash
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Route                      | Description        |
| ------ | -------------------------- | ------------------ |
| POST   | /login/register_candidate  | Register Candidate |
| POST   | /login/register_recruiter  | Register Recruiter |
| POST   | /login/candidate           | Candidate Login    |
| POST   | /login/recruiter           | Recruiter Login    |
| GET    | /jobs/                     | Get All Jobs       |
| POST   | /jobs/apply                | Apply for Job      |
| GET    | /jobs/applied_jobs         | Get Applied Jobs   |
| POST   | /add_jobs                  | Add New Job        |
| DELETE | /delete_job/{job_id}       | Delete Job         |
| GET    | /{recruiter_id}/applicants | Get Applicants     |
