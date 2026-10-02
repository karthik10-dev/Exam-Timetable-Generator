import collections
from flask import Flask, render_template, request
from scheduler_engine import BacktrackingExamScheduler


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/demo")
def demo():
    return render_template(
        "index.html",
        preset_dates="2026-10-01, 2026-10-03, 2026-10-05, 2026-10-07",
        preset_slot="09:30 AM - 12:30 PM",
        preset_branches="Computer Science: Mathematics I, Data Structures, Operating Systems, Computer Networks\nElectrical Eng: Mathematics I, Circuit Analysis, Digital Electronics, Signals & Systems\nMechanical Eng: Mathematics I, Thermodynamics, Fluid Mechanics, Engineering Mechanics",
        preset_restricted="Thermodynamics: 2026-10-01, Operating Systems: 2026-10-01",
        preset_diff="Mathematics I: 3, Operating Systems: 2, Thermodynamics: 3, Circuit Analysis: 2"
    )


@app.route("/generate", methods=["POST"])
def generate():
    try:
        raw_dates = request.form.get("available_dates", "").strip()
        time_slot = request.form.get(
            "time_slot", "09:30 AM - 12:30 PM"
        ).strip()
        raw_branches = request.form.get("branch_data", "").strip()
        raw_blocked = request.form.get("restricted_dates", "").strip()
        raw_diff = request.form.get("difficulty_ratings", "").strip()

        dates = [date.strip() for date in raw_dates.split(",") if date.strip()]

        branches = {}
        all_subjects = []

        for line in raw_branches.splitlines():
            if ":" not in line:
                continue

            branch, subjects = line.split(":", 1)
            branch = branch.strip()
            subjects = [
                subject.strip()
                for subject in subjects.split(",")
                if subject.strip()
            ]

            if branch and subjects:
                branches[branch] = subjects
                all_subjects.extend(subjects)

        counts = collections.Counter(all_subjects)
        common = [
            subject for subject, count in counts.items()
            if count > 1
        ]

        blocked = {}

        if raw_blocked:
            for item in raw_blocked.split(","):
                if ":" not in item:
                    continue

                subject, date = item.split(":", 1)
                subject = subject.strip()
                date = date.strip()

                if subject not in blocked:
                    blocked[subject] = []

                blocked[subject].append(date)

        difficulty = {}

        if raw_diff:
            for item in raw_diff.split(","):
                if ":" not in item:
                    continue

                subject, level = item.split(":", 1)
                subject = subject.strip()
                level = level.strip()

                if level.isdigit():
                    level = int(level)
                    difficulty[subject] = max(1, min(3, level))

        if not dates or not branches:
            return render_template(
                "error.html",
                error_message="Please enter at least one date and one branch with subjects."
            )

        scheduler = BacktrackingExamScheduler(
            dates,
            time_slot,
            branches,
            common,
            blocked,
            difficulty
        )

        schedule, score = scheduler.find_schedule()

        if schedule is None:
            return render_template(
                "error.html",
                error_message="No valid timetable could be generated. Please check the available dates and subjects."
            )

        rows = []

        for branch, subjects in branches.items():
            cells = {date: None for date in dates}

            for (subject, branch_name), date in schedule.items():
                if branch_name == branch:
                    level = difficulty.get(subject, 2)

                    cells[date] = {
                        "subject": subject,
                        "difficulty": level,
                        "is_common": subject in common
                    }

            rows.append({
                "branch": branch,
                "cells": cells
            })

        return render_template(
            "timetable.html",
            time_slot=time_slot,
            header_dates=dates,
            matrix_rows=rows
        )

    except Exception as error:
        return render_template(
            "error.html",
            error_message=f"An error occurred: {error}"
        )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
