<<<<<<< HEAD
# Examination Timetable Generator

A small Flask web app that generates examination timetables from available dates, branch subjects, subject restrictions, and difficulty ratings.

## Requirements

- Python 3.7 or newer (the scheduler uses dataclasses).
- Flask

## Setup

Create and activate a virtual environment, then install Flask:

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependency and start the app:

```bash
python -m pip install Flask
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. The built-in Flask server runs in debug mode and is intended for local development only.

## Using the app

1. Enter available examination dates separated by commas. ISO dates such as `2026-10-01` are recommended.
2. Enter the daily time slot.
3. Enter one branch per line, with subjects separated by commas:

   ```text
   Computer Science: Mathematics I, Data Structures, Operating Systems
   Electrical Eng: Mathematics I, Circuit Analysis, Digital Electronics
   ```

4. Optionally, list restricted dates as comma-separated `Subject: Date` pairs:

   ```text
   Operating Systems: 2026-10-01, Thermodynamics: 2026-10-03
   ```

5. Optionally, assign subject difficulty ratings from 1 (Easy) to 3 (Difficult):

   ```text
   Mathematics I: 3, Operating Systems: 2
   ```

6. Select **Generate Timetable** to view the schedule. Use **Load Demo Setup** on the home page to populate sample input.

Subjects repeated across branches are treated as common subjects and scheduled on the same date. A branch cannot have more than one exam on a date. Restricted dates apply to every occurrence of that subject. If a valid schedule cannot be generated, add dates or review the restrictions.

## Project files

- `app.py` — Flask routes and form processing.
- `scheduler_engine.py` — timetable constraint and scheduling logic.
- `templates/` — input, timetable, and error pages.
=======
# Exam-Timetable-Generator
An AI-based web application that automatically generates examination timetables for multiple branches using Constraint Satisfaction, Backtracking, and Hill Climbing. It handles hard constraints such as subject conflicts, common-subject synchronization, available dates, and restricted dates, while improving the timetable using soft constraints.
>>>>>>> ea114c00decd2704695c2355245841ca543a3978
