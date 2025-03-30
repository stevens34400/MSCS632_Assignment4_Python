from typing import Dict, List
import sys
from schedule_constants import *
from scheduler import generate_schedule
from storage import save_data, load_data

def print_schedule(schedule: Dict):
    if not schedule:
        print("No schedule available.")
        return

    print("\nCurrent Schedule:")
    print("-" * 80)
    for day in DAYS_OF_WEEK:
        print(f"\n{day}:")
        for shift in SHIFTS:
            employees = schedule[day][shift]
            print(f"  {shift}: {', '.join(employees) if employees else 'No assignments'}")
    print("-" * 80)

def input_preferences() -> Dict[str, List[str]]:
    preferences = {}
    for day in DAYS_OF_WEEK:
        print(f"\nEnter shift preferences for {day} (comma-separated):")
        print(f"Available shifts: {', '.join(SHIFTS)}")
        while True:
            prefs = input("Enter preferences: ").strip().split(',')
            prefs = [p.strip() for p in prefs if p.strip() in SHIFTS]
            if prefs:
                preferences[day] = prefs
                break
            print("Invalid preferences. Please try again.")
    return preferences

def add_employee(employees: List[Dict]) -> List[Dict]:
    print("\nAdding new employee")
    name = input("Enter employee name: ").strip()
    
    if any(emp["name"] == name for emp in employees):
        print("Employee already exists!")
        return employees

    preferences = input_preferences()
    employees.append({"name": name, "preferences": preferences})
    return employees

def main():
    employees, schedule = load_data()

    while True:
        print("\nEmployee Scheduler")
        print("1. Add Employee")
        print("2. Generate Schedule")
        print("3. View Schedule")
        print("4. Clear All Data")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            employees = add_employee(employees)
            save_data(employees, schedule)
        
        elif choice == "2":
            if not employees:
                print("Please add at least one employee first!")
                continue
            schedule = generate_schedule(employees)
            save_data(employees, schedule)
            print_schedule(schedule)
        
        elif choice == "3":
            print_schedule(schedule)
        
        elif choice == "4":
            confirm = input("Are you sure you want to clear all data? (y/n): ").lower()
            if confirm == 'y':
                employees = []
                schedule = None
                save_data(employees, schedule)
                print("All data cleared.")
        
        elif choice == "5":
            print("Goodbye!")
            sys.exit(0)
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 