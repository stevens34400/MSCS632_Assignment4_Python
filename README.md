# MSCS632_Assignment4_Python

A Python-based Employee Scheduling System that helps manage and generate work schedules based on employee preferences and scheduling constraints.

## Features

- Add new employees with their shift preferences
- Generate optimized work schedules
- View current schedule
- Persistent data storage
- Clear all data when needed

## System Constraints

- Days: Monday through Sunday
- Shifts: Morning, Afternoon, Evening
- Maximum 1 shift per employee per day
- Minimum 2 employees per shift
- Maximum 5 working days per employee

## Installation

1. Clone this repository
2. Ensure you have Python installed
3. No additional dependencies required - uses only Python standard library

## Usage

Run the program using:
```python
python main.py
```

### Menu Options

1. **Add Employee**: Add a new employee with their shift preferences for each day
2. **Generate Schedule**: Create a new schedule based on employee preferences and constraints
3. **View Schedule**: Display the current schedule
4. **Clear All Data**: Reset all employee and schedule data
5. **Exit**: Close the application

## File Structure

- `main.py`: Main program interface and control flow
- `scheduler.py`: Schedule generation logic
- `storage.py`: Data persistence handling
- `schedule_constants.py`: System constants and constraints
- `employee_data.json`: Persistent storage for employee and schedule data

## How It Works

The scheduler attempts to create an optimal schedule by:
1. First assigning employees to their preferred shifts
2. Finding alternative slots when preferred shifts are full
3. Filling remaining slots while respecting system constraints
4. Storing all data persistently between sessions

## Data Storage

Employee data and schedules are stored in `employee_data.json` and persist between program runs. 