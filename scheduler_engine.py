import copy
import random
from dataclasses import dataclass


@dataclass
class ExamSubject:
    code: str
    branch: str
    difficulty: int = 3
    blocked: list = None
    common: bool = False


class BacktrackingExamScheduler:

    def __init__(self, dates, time_slot, branch_subjects, common_subjects,
                 blocked_dates=None, difficulty=None):

        self.dates = sorted(set(dates))
        self.time_slot = time_slot
        self.branch_subjects = branch_subjects
        self.common_subjects = set(common_subjects or [])
        self.blocked_dates = blocked_dates or {}
        self.difficulty = difficulty or {}

        self.subjects = []
        self.all_subjects = set()

        for branch, subjects in branch_subjects.items():
            for subject in subjects:
                subject = subject.strip()

                if not subject:
                    continue

                self.all_subjects.add(subject)

                self.subjects.append(
                    ExamSubject(
                        code=subject,
                        branch=branch,
                        difficulty=self.difficulty.get(subject, 3),
                        blocked=self.blocked_dates.get(subject, []),
                        common=subject in self.common_subjects
                    )
                )

    def get_score(self, schedule):
        score = 0
        logs = {}
        branch_dates = {}

        for (subject, branch), date in schedule.items():
            if branch not in branch_dates:
                branch_dates[branch] = []
            branch_dates[branch].append(date)

        for branch, dates in branch_dates.items():
            indexes = sorted(
                self.dates.index(date)
                for date in dates
                if date in self.dates
            )

            for i in range(len(indexes) - 1):
                gap = indexes[i + 1] - indexes[i]

                if gap == 1:
                    score -= 10
                elif gap >= 2:
                    score += 10

        for (sub1, branch1), date1 in schedule.items():
            if self.difficulty.get(sub1, 3) < 4:
                continue

            for (sub2, branch2), date2 in schedule.items():
                if (sub1, branch1) == (sub2, branch2):
                    continue

                if branch1 != branch2:
                    continue

                if self.difficulty.get(sub2, 3) < 4:
                    continue

                if abs(self.dates.index(date1) - self.dates.index(date2)) == 1:
                    score -= 15

        for branch, dates in branch_dates.items():
            count = max((dates.count(date) for date in self.dates), default=0)

            if count <= 1:
                score += 15

        return {"total_score": score, "logs": logs}

    def is_valid(self, subject, date, schedule):
        if subject.blocked and date in subject.blocked:
            return False

        for (code, branch), old_date in schedule.items():
            if branch == subject.branch and old_date == date:
                return False

            if subject.common and code == subject.code and old_date != date:
                return False

        return True

    def find_schedule(self):
        schedule = {}
        subjects = list(self.subjects)

        subjects.sort(key=lambda x: (not x.common, x.code))

        ok, result = self.backtrack(subjects, schedule)

        if not ok:
            return None, {
                "message": "Could not create a timetable.",
                "score_info": None
            }

        result, score = self.improve(result)
        return result, score

    def backtrack(self, subjects, schedule):
        if not subjects:
            return True, schedule

        subject = subjects[0]

        for date in self.dates:
            if self.is_valid(subject, date, schedule):
                key = (subject.code, subject.branch)
                schedule[key] = date

                ok, result = self.backtrack(subjects[1:], schedule)

                if ok:
                    return True, result

                del schedule[key]

        return False, None

    def improve(self, schedule, tries=150):
        best = copy.copy(schedule)
        best_score = self.get_score(best)

        movable = [
            (subject.code, subject.branch)
            for subject in self.subjects
            if not subject.common
        ]

        if not movable:
            return best, best_score

        for _ in range(tries):
            key = random.choice(movable)
            subject = next(
                item for item in self.subjects
                if (item.code, item.branch) == key
            )

            old_date = best[key]
            choices = [date for date in self.dates if date != old_date]

            if not choices:
                continue

            new_date = random.choice(choices)
            test = copy.copy(best)
            del test[key]

            if self.is_valid(subject, new_date, test):
                test[key] = new_date
                score = self.get_score(test)

                if score["total_score"] > best_score["total_score"]:
                    best = test
                    best_score = score

        return best, best_score
