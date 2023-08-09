import csv
# Greedy Scheduler that always produces a shift

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

def assign_shift(worker, shift):
    shift.append(worker)

def remove_shift_assignment(worker, shift):
    if worker in shift:
        shift.remove(worker)

def is_schedule_valid(schedule, required_hours=8):
    total_hours = sum(calculate_shift_hours(shift) for shift in schedule)
    return total_hours >= required_hours

def create_schedule(schedule_data, shifts_per_day=10, overlapping_shifts=5):
    prioritized_workers = get_prioritized_workers(schedule_data)
    remaining_workers = get_remaining_workers(schedule_data)
    all_workers = prioritized_workers + remaining_workers
    num_shifts = shifts_per_day

    schedule = [[] for _ in range(num_shifts)]
    unassigned_workers = []

    # Assign prioritized workers first
    for worker in prioritized_workers:
        assigned = False
        for shift in schedule:
            if not is_shift_full(shift) and is_worker_available(worker, shift):
                assign_shift(worker, shift)
                assigned = True
                break
        if not assigned:
            unassigned_workers.append(worker)

    # Assign remaining workers
    for worker in remaining_workers:
        assigned = False
        for shift in schedule:
            if not is_shift_full(shift) and is_worker_available(worker, shift):
                assign_shift(worker, shift)
                assigned = True
                break
        if not assigned:
            unassigned_workers.append(worker)

    return schedule, unassigned_workers

if __name__ == "__main__":
    schedule_data = read_csv_file("schedule_data.csv")
    if not isinstance(schedule_data, list):
        print("Error: CSV data is not formatted correctly.")
    else:
        schedule, unassigned_workers = create_schedule(schedule_data)
        if is_schedule_valid(schedule):
            for idx, shift in enumerate(schedule):
                print(f"Shift {idx + 1}:")
                for worker in shift:
                    print(f"{worker['Name']} (Position: {worker['Position']}, Priority: {worker['Priority']})")
                print("-------------")
        else:
            print("No valid schedule found.")

        counter = 0
        if unassigned_workers:
            print("\nUnassigned Workers:")
            for worker in unassigned_workers:
                print(f"{worker['Name']} (Position: {worker['Position']}, Priority: {worker['Priority']})")
                counter+=1
        print(f"\nUnassigned workers: {counter}")
