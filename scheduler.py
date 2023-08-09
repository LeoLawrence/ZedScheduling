import csv
from datetime import datetime, timedelta

# this is closer to a fair scheduler since everyone ends up getting shifts properly. There's very little overlap though.

# Helper function to parse datetime
def parse_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %I:%M %p")

# Load schedule data
schedule_data = []
with open('schedule_data.csv', newline='') as schedule_file:
    schedule_reader = csv.DictReader(schedule_file)
    for row in schedule_reader:
        row['Priority'] = int(row['Priority'])  # Convert 'Priority' to an integer
        schedule_data.append(row)

# Load shifts data
shifts = []
with open('shifts.csv', newline='') as shifts_file:
    shifts_reader = csv.DictReader(shifts_file)
    for row in shifts_reader:
        start_datetime = parse_datetime(row['Start DateTime'])
        end_datetime = parse_datetime(row['End DateTime'])
        shift_duration = (end_datetime - start_datetime).total_seconds() / 3600
        shifts.append({
            'Location': row['Location'],
            'Position': row['Position'],
            'Start DateTime': start_datetime,
            'End DateTime': end_datetime,
            'Duration': shift_duration
        })

# Sort the shifts by start time
shifts.sort(key=lambda x: x['Start DateTime'])

# Create a schedule dictionary to store assigned shifts for each worker
schedule = {worker['Name']: [] for worker in schedule_data}

# Function to check if a worker is available for a shift
def is_worker_available(worker, shift):
    return worker['Position'] == shift['Position'] and shift['Start DateTime'] not in [assigned_shift['Start DateTime'] for assigned_shift in schedule[worker['Name']]]

# Function to assign a shift to a worker
def assign_shift(worker, shift):
    min_shifts_assigned_worker = min(schedule, key=lambda w: len(schedule[w]))
    schedule[min_shifts_assigned_worker].append(shift)

# Function to remove a shift assignment from a worker
def remove_shift_assignment(worker, shift):
    schedule[worker['Name']].remove(shift)

# Function to find an optimal schedule using a greedy approach
def find_optimal_schedule(workers, shifts):
    shifts_assigned = 0
    for shift in shifts:
        available_workers = [worker for worker in workers if is_worker_available(worker, shift)]
        if not available_workers:
            continue

        assign_shift(None, shift)  # Use None as a placeholder for the worker since it will be determined in the assign_shift() function
        shifts_assigned += 1

    return shifts_assigned

# Find the optimal schedule using a greedy approach
optimal_schedule = find_optimal_schedule(schedule_data, shifts)
print(f"Number of shifts assigned: {optimal_schedule}")

# Calculate the number of workers who did not get shifts
workers_without_shifts = len(schedule_data) - len([worker for worker in schedule_data if len(schedule[worker['Name']]) > 0])
print(f"Number of workers without shifts: {workers_without_shifts}")

# Output the schedule for each worker
for worker, assigned_shifts in schedule.items():
    print(f"{worker}: {len(assigned_shifts)} shifts")
    for shift in assigned_shifts:
        print(f"  {shift['Location']} ({shift['Position']}): {shift['Start DateTime'].strftime('%Y-%m-%d %I:%M %p')} - {shift['End DateTime'].strftime('%I:%M %p')}")
