# Student Result Management System

A full-stack web application that allows schools to manage students, subjects, marks, and generate result cards with grade calculations.

---

## Features

- School registration and login with JWT authentication
- Add and manage students and subjects
- Enter and update marks per student per subject
- Auto-calculated grades and percentages
- Student result card with subject-wise breakdown
- Class report with rankings, topper, and average
- Multi-school support (each school sees only its own data)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 |
| Authentication | JWT (python-jose), bcrypt (passlib) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Server | Uvicorn (ASGI) |

---

## Project Structure

```
student-result-system/
├── backend/
│   ├── main.py              # App entry point, CORS, router registration
│   ├── database.py          # PostgreSQL connection, session setup
│   ├── models.py            # SQLAlchemy table models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── auth.py              # JWT token creation and verification
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables (not committed)
│   └── routers/
│       ├── auth.py          # Register, login endpoints
│       ├── students.py      # Student CRUD endpoints
│       ├── subjects.py      # Subject CRUD endpoints
│       ├── marks.py         # Mark entry endpoints
│       └── results.py       # Result card and class report endpoints
└── frontend/
    ├── index.html           # Login and Register page
    ├── dashboard.html       # Dashboard with stats
    ├── students.html        # Add and view students
    ├── subjects.html        # Add and view subjects
    ├── marks.html           # Enter and view marks
    ├── results.html         # Result card and class report
    ├── css/
    │   └── style.css        # All styles
    └── js/
        └── api.js           # API calls, token management
```

---

## Database Schema

```sql
schools    (id, name, email, password, created_at)
students   (id, school_id, name, roll_no, class_name, created_at)
subjects   (id, school_id, name, total_marks)
marks      (id, student_id, subject_id, obtained_marks, created_at)
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new school |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current school info |
| POST | `/students/` | Add a student |
| GET | `/students/` | List all students |
| DELETE | `/students/{id}` | Delete a student |
| POST | `/subjects/` | Add a subject |
| GET | `/subjects/` | List all subjects |
| DELETE | `/subjects/{id}` | Delete a subject |
| POST | `/marks/` | Enter or update marks |
| GET | `/marks/student/{id}` | Get marks for a student |
| GET | `/results/student/{id}` | Get full result card |
| GET | `/results/class/{name}/topper` | Get class topper |
| GET | `/results/class/{name}/report` | Get full class report |

---

## Grade Scale

| Percentage | Grade |
|---|---|
| 90% and above | A+ |
| 80% – 89% | A |
| 70% – 79% | B |
| 60% – 69% | C |
| 50% – 59% | D |
| Below 50% | F |

---

## Prerequisites

- Python 3.11+
- PostgreSQL installed and running

---

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Haani76/student-result-system.git
cd student-result-system
```

### 2. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Set up PostgreSQL

Create a database:
```sql
CREATE DATABASE student_db;
```

### 4. Configure environment variables

Create a `.env` file inside the `backend/` folder:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:YOUR_PORT/student_db
SECRET_KEY=supersecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Replace `YOUR_PASSWORD` and `YOUR_PORT` with your PostgreSQL credentials.

### 5. Run the backend server

```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8080 --reload
```

The API will be available at `http://localhost:8080`  
Interactive API docs at `http://localhost:8080/docs`

### 6. Open the frontend

Open `frontend/index.html` directly in your browser.  
Register your school, then start adding students and subjects.

---

## How to Use

1. **Register** your school with a name, email, and password
2. Go to **Subjects** — add subjects like Mathematics, English, Physics
3. Go to **Students** — add students with name, roll number, and class
4. Go to **Enter Marks** — select a student and subject, enter obtained marks
5. Go to **Results** — select a student to view their result card, or enter a class name to see the full class report with rankings

---

## Contributors

- [Haani76](https://github.com/Haani76)
