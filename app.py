from flask import Flask, render_template, request

app = Flask(__name__)

def grade_to_points(grade):
    grades = {
        'A': 4.0, 'A-': 3.7, 'B+': 3.3,
        'B': 3.0, 'B-': 2.7, 'C+': 2.3,
        'C': 2.0, 'C-': 1.7, 'D+': 1.3,
        'D': 1.0, 'F': 0.0
    }
    return grades.get(grade.upper())

def calculate_new_cgpa(current_cgpa, total_credits, old_grade, course_credits, new_grade):
    old_points = grade_to_points(old_grade)
    new_points = grade_to_points(new_grade)

    if old_points is None or new_points is None:
        return None

    current_total_points = current_cgpa * total_credits
    updated_total = current_total_points - (old_points * course_credits) + (new_points * course_credits)
    return round(updated_total / total_credits, 3)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            current_cgpa = float(request.form['current_cgpa'])
            total_credits = int(request.form['total_credits'])
            old_grade = request.form['old_grade']
            course_credits = int(request.form['course_credits'])
            new_grade = request.form['new_grade']

            new_cgpa = calculate_new_cgpa(current_cgpa, total_credits, old_grade, course_credits, new_grade)
            if new_cgpa is None:
                error = "Invalid grade entered. Please try again."
                return render_template('index.html', error=error)

            return render_template('result.html', new_cgpa=new_cgpa)
        except ValueError:
            error = "Please enter valid numeric values."
            return render_template('index.html', error=error)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)