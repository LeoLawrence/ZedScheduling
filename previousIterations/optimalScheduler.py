import csv
from itertools import combinations
import copy

# Uses Backtracking to find an optimal schedule.

def read_csv_file(file_path):
    schedule_data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['Priority'] = int(row['Priority'])  # Convert 'Priority' to an integer
            schedule_data.append(row)
    return schedule_data

def get_prioritized_workers(schedule_data):
    prioritized_workers = [worker for worker in schedule_data if worker['Priority'] == 5]
    return prioritized_workers

def get_remaining_workers(schedule_data):
    remaining_workers = [worker for worker in schedule_data if worker['Priority'] < 5]
    return remaining_workers

def calculate_shift_hours(shift):
    return 2.5 * len(shift)

def is_shift_full(shift):
    return len(shift) == 2

def is_worker_available(worker, shift):
    if not shift:
        # If the shift is empty, assume the default position is 'L1' (or 'L2', whichever is appropriate)
        default_position = 'L1'
        return worker['Position'] != default_position

    position = shift[0]['Position']
    return worker['Position'] != position

def can_assign_shift(worker, shift):
    if is_shift_full(shift) or not is_worker_available(worker, shift):
        return False
    return True

def assign_shift(worker, shift):
    shift.append(worker)

def remove_shift_assignment(worker, shift):
    if worker in shift:
        shift.remove(worker)


def is_schedule_valid(schedule):
    total_hours = sum(calculate_shift_hours(shift) for shift in schedule)
    return 8 <= total_hours <= 12

def find_optimal_schedule(schedule_data, shifts_per_day=10, overlapping_shifts=5):
    prioritized_workers = get_prioritized_workers(schedule_data)
    remaining_workers = get_remaining_workers(schedule_data)
    all_workers = prioritized_workers + remaining_workers
    num_shifts = len(schedule_data) // shifts_per_day

    schedule = [[] for _ in range(num_shifts)]

    def backtrack(shift_index):
        if shift_index == num_shifts:
            return is_schedule_valid(schedule)

        for shift_combination in combinations(range(len(all_workers)), overlapping_shifts):
            for worker_index in shift_combination:
                worker = all_workers[worker_index]
                if can_assign_shift(worker, schedule[shift_index]):
                    assign_shift(worker, schedule[shift_index])
                else:
                    break
            else:
                if backtrack(shift_index + 1):
                    return True
            for worker_index in shift_combination:
                worker = all_workers[worker_index]
                remove_shift_assignment(worker, schedule[shift_index])

        return False

    if backtrack(0):
        return schedule
    return None

if __name__ == "__main__":
    schedule_data = read_csv_file("schedule_data.csv")
    if not isinstance(schedule_data, list):
        print("Error: CSV data is not formatted correctly.")
    else:
        optimal_schedule = find_optimal_schedule(schedule_data)
        if optimal_schedule:
            for idx, shift in enumerate(optimal_schedule):
                print(f"Shift {idx + 1}:")
                for worker in shift:
                    print(f"{worker['Name']} (Position: {worker['Position']}, Priority: {worker['Priority']})")
                print("-------------")
        else:
            print("No valid schedule found.")
