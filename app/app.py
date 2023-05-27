from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

# Constants for pagination
PAGE_SIZE = 10

def load_student_details():
    # Load student details from a CSV file
    students = []
    with open('student_details.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append(row)
    return students

def filter_students(students, filter_criteria):
    # Apply the filters to the student data
    filtered_students = []
    for student in students:
        if student_matches_criteria(student, filter_criteria):
            filtered_students.append(student)
    return filtered_students

def student_matches_criteria(student, filter_criteria):
    # Filter based on student name and total marks
    name_filter = filter_criteria.get("name")
    marks_filter = filter_criteria.get("marks")

    if name_filter and student["name"].lower().find(name_filter.lower()) == -1:
        return False

    if marks_filter and int(student["total_marks"]) < int(marks_filter):
        return False

    return True

@app.route("/students", methods=["GET"])
def get_students():
    # Get page number from query parameter
    page = int(request.args.get("page", 1))

    # Load student details from the file
    students = load_student_details()

    # Calculate start and end indices for pagination
    start_index = (page - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE

    # Retrieve the students for the requested page
    paginated_students = students[start_index:end_index]

    return jsonify(paginated_students)

@app.route("/students/filter", methods=["POST"])
def filter_students_endpoint():
    # Get filter criteria from request body
    filter_criteria = request.json

    # Load student details from the file
    students = load_student_details()

    # Apply filters to the student data
    filtered_students = filter_students(students, filter_criteria)

    return jsonify(filtered_students)

if __name__ == "__main__":
    app.run()
