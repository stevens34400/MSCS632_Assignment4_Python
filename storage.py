import json
import os

STORAGE_FILE = "employee_data.json"

# Save the employee data and schedule to a JSON file
def save_data(employees, schedule=None):
    data = {
        "employees": employees,
        "schedule": schedule
    }
    with open(STORAGE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Load the employee data and schedule from a JSON file
def load_data():
    if not os.path.exists(STORAGE_FILE):
        return [], None
    
    with open(STORAGE_FILE, 'r') as f:
        data = json.load(f)
        return data.get("employees", []), data.get("schedule", None) 