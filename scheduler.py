from typing import Dict, List, Set
import random
from schedule_constants import *

# Find the next available shift for an employee
def find_next_available_shift(
    schedule: Dict,
    day: str,
    employee_name: str,
    employee_days_worked: Dict[str, int],
    employee_assigned_days: Dict[str, Set[str]]
) -> Dict:
    # Check other shifts on the same day
    for shift in SHIFTS:
        if (len(schedule[day][shift]) < MIN_EMPLOYEES_PER_SHIFT and
            employee_name not in schedule[day][shift]):
            return {"day": day, "shift": shift}

    # Check next day's shifts
    next_day_index = (DAYS_OF_WEEK.index(day) + 1) % len(DAYS_OF_WEEK)
    next_day = DAYS_OF_WEEK[next_day_index]

    if next_day not in employee_assigned_days[employee_name]:
        for shift in SHIFTS:
            if len(schedule[next_day][shift]) < MIN_EMPLOYEES_PER_SHIFT:
                return {"day": next_day, "shift": shift}

    return None

# Generate a schedule for the employees based on their preferences
def generate_schedule(employees: List[Dict]) -> Dict:
    # Initialize schedule
    schedule = {day: {shift: [] for shift in SHIFTS} for day in DAYS_OF_WEEK}

    # Track employee assignments
    employee_days_worked = {emp["name"]: 0 for emp in employees}
    employee_assigned_days = {emp["name"]: set() for emp in employees}

    # First pass: Assign employees based on primary preferences
    for day in DAYS_OF_WEEK:
        for shift in SHIFTS:
            eligible_employees = [
                emp for emp in employees
                if (day in emp["preferences"] and
                    emp["preferences"][day][0] == shift and
                    employee_days_worked[emp["name"]] < MAX_DAYS_PER_EMPLOYEE and
                    day not in employee_assigned_days[emp["name"]])
            ]

            # Sort by preference ranking
            eligible_employees.sort(
                key=lambda x: x["preferences"][day].index(shift)
            )

            for emp in eligible_employees:
                if len(schedule[day][shift]) < MIN_EMPLOYEES_PER_SHIFT:
                    schedule[day][shift].append(emp["name"])
                    employee_days_worked[emp["name"]] += 1
                    employee_assigned_days[emp["name"]].add(day)
                else:
                    # Handle conflict: preferred shift is full
                    alternative = find_next_available_shift(
                        schedule, day, emp["name"],
                        employee_days_worked, employee_assigned_days
                    )
                    
                    if alternative and employee_days_worked[emp["name"]] < MAX_DAYS_PER_EMPLOYEE:
                        alt_day, alt_shift = alternative["day"], alternative["shift"]
                        schedule[alt_day][alt_shift].append(emp["name"])
                        employee_days_worked[emp["name"]] += 1
                        employee_assigned_days[emp["name"]].add(alt_day)

    # Second pass: Fill remaining slots
    for day in DAYS_OF_WEEK:
        for shift in SHIFTS:
            while len(schedule[day][shift]) < MIN_EMPLOYEES_PER_SHIFT:
                available_employees = [
                    emp for emp in employees
                    if (employee_days_worked[emp["name"]] < MAX_DAYS_PER_EMPLOYEE and
                        day not in employee_assigned_days[emp["name"]] and
                        day in emp["preferences"] and
                        shift in emp["preferences"][day])
                ]

                if not available_employees:
                    # Try to find any available employee
                    any_available = [
                        emp for emp in employees
                        if (employee_days_worked[emp["name"]] < MAX_DAYS_PER_EMPLOYEE and
                            day not in employee_assigned_days[emp["name"]])
                    ]

                    if not any_available:
                        break

                    emp = random.choice(any_available)
                else:
                    # Sort by preference ranking
                    available_employees.sort(
                        key=lambda x: x["preferences"][day].index(shift)
                    )
                    emp = available_employees[0]

                schedule[day][shift].append(emp["name"])
                employee_days_worked[emp["name"]] += 1
                employee_assigned_days[emp["name"]].add(day)

    return schedule 