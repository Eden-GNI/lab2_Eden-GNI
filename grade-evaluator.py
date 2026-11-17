import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def validate_scores(data):
    """Returns True if every score is between 0 and 100, otherwise False."""
    all_valid = True
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(f"Error: Invalid score {item['score']} for '{item['assignment']}'. "
                  f"Scores must be between 0 and 100.")
            all_valid = False
    return all_valid

def validate_weights(data):
    """Returns True if the weights add up correctly, otherwise False."""
    total_weight = 0
    summative_weight = 0
    formative_weight = 0

    for item in data:
        total_weight += item['weight']
        if item['group'] == 'Summative':
            summative_weight += item['weight']
        elif item['group'] == 'Formative':
            formative_weight += item['weight']

    all_valid = True

    if round(total_weight, 2) != 100:
        print(f"Error: Total weight is {total_weight}, but it must be exactly 100.")
        all_valid = False
    if round(summative_weight, 2) != 40:
        print(f"Error: Summative weight is {summative_weight}, but it must be exactly 40.")
        all_valid = False
    if round(formative_weight, 2) != 60:
        print(f"Error: Formative weight is {formative_weight}, but it must be exactly 60.")
        all_valid = False

    return all_valid

def calculate_grades(data):
    """
    Returns (total_grade, gpa, formative_points, summative_points).
    Each assignment contributes: score * weight / 100
    """
    formative_points = 0
    summative_points = 0

    for item in data:
        points = item['score'] * item['weight'] / 100
        if item['group'] == 'Formative':
            formative_points += points
        elif item['group'] == 'Summative':
            summative_points += points

    total_grade = formative_points + summative_points
    gpa = (total_grade / 100) * 5.0

    return total_grade, gpa, formative_points, summative_points

def determine_status(formative_points, summative_points):
    """
    Returns (status, formative_pct, summative_pct).
    Status is 'PASSED' only if BOTH categories are >= 50%.
    """
    formative_pct = formative_points / 60 * 100
    summative_pct = summative_points / 40 * 100

    if formative_pct >= 50 and summative_pct >= 50:
        status = "PASSED"
    else:
        status = "FAILED"

    return status, formative_pct, summative_pct

def find_resubmissions(data):
    """
    Returns a list of failed formative assignments (score < 50)
    that share the highest weight among the failed ones.
    """
    failed = []
    for item in data:
        if item['group'] == 'Formative' and item['score'] < 50:
            failed.append(item)

    if not failed:
        return []

    highest_weight = max(item['weight'] for item in failed)

    resubmit = []
    for item in failed:
        if item['weight'] == highest_weight:
            resubmit.append(item)

    return resubmit

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")

    if not validate_scores(data):
	  return

    if not validate_weights(data):
	return

    total_grade, gpa, formative_points, summative_points = calculate_grades(data)
    status, formative_pct, summative_pct = determine_status(formative_points, summative_points)
    resubmit = find_resubmissions(data)

    print(f"Total Grade: {total_grade:.2f}%")
    print(f"GPA: {gpa:.2f}")
    print(f"Formative: {formative_pct:.2f}%")
    print(f"Summative: {summative_pct:.2f}%")
    print(f"\nFinal Status: {status}")

    if resubmit:
        print("\nEligible for resubmission (failed formative with the highest weight):")
        for item in resubmit:
            print(f"  - {item['assignment']} (score: {item['score']:.0f}, weight: {item['weight']:.0f})")
    else:
        print("\nNo failed formative assignments. No resubmission needed.")

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
