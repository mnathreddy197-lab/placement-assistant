from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = "placement-assistant-secret"


def create_database():
    connection = sqlite3.connect("placement.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            college TEXT NOT NULL,
            branch TEXT NOT NULL,
            cgpa REAL,
            programming_language TEXT,
            career_goal TEXT
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        name = request.form["name"]
        college = request.form["college"]
        branch = request.form["branch"]
        cgpa = request.form["cgpa"]
        programming_language = request.form["programming_language"]
        career_goal = request.form["career_goal"]

        connection = sqlite3.connect("placement.db")

        connection.execute("""
            INSERT INTO students
            (name, college, branch, cgpa, programming_language, career_goal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            college,
            branch,
            cgpa,
            programming_language,
            career_goal
        ))

        connection.commit()
        connection.close()

        session["student_name"] = name

        return redirect_dashboard()

    return render_template("profile.html")


def redirect_dashboard():
    return render_template(
        "dashboard.html",
        name=session.get("student_name", "Student"),
        aptitude_score=session.get("aptitude_score", 0),
        coding_score=session.get("coding_score", 0),
        interview_status=session.get(
            "interview_status",
            "Not Completed"
        ),
        resume_status=session.get(
            "resume_status",
            "Not Completed"
        ),
        readiness_score=calculate_readiness()
    )


def calculate_readiness():
    aptitude_score = int(session.get("aptitude_score", 0))
    coding_score = int(session.get("coding_score", 0))

    score = 0

    score += aptitude_score * 5
    score += coding_score * 5

    if session.get("interview_status") == "Completed":
        score += 25

    if session.get("resume_status") == "Completed":
        score += 25

    return score


@app.route("/dashboard")
def dashboard():
    return redirect_dashboard()


@app.route("/aptitude", methods=["GET", "POST"])
def aptitude():
    if request.method == "POST":
        score = 0

        if request.form.get("q1") == "40":
            score += 1

        if request.form.get("q2") == "60":
            score += 1

        if request.form.get("q3") == "30":
            score += 1

        if request.form.get("q4") == "25":
            score += 1

        if request.form.get("q5") == "10":
            score += 1

        session["aptitude_score"] = score

        return render_template(
            "aptitude_result.html",
            score=score
        )

    return render_template("aptitude.html")


@app.route("/coding", methods=["GET", "POST"])
def coding():
    if request.method == "POST":
        score = 0

        if request.form.get("q1") == "def":
            score += 1

        if request.form.get("q2") == "boolean":
            score += 1

        if request.form.get("q3") == "a":
            score += 1

        if request.form.get("q4") == "#":
            score += 1

        if request.form.get("q5") == "css":
            score += 1

        session["coding_score"] = score

        return render_template(
            "coding_result.html",
            score=score
        )

    return render_template("coding.html")


@app.route("/resume", methods=["GET", "POST"])
def resume():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        college = request.form["college"]
        branch = request.form["branch"]
        cgpa = request.form["cgpa"]
        skills = request.form["skills"]
        objective = request.form["objective"]

        session["resume_status"] = "Completed"

        return render_template(
            "resume_result.html",
            name=name,
            email=email,
            phone=phone,
            college=college,
            branch=branch,
            cgpa=cgpa,
            skills=skills,
            objective=objective
        )

    return render_template("resume.html")


@app.route("/interview", methods=["GET", "POST"])
def interview():
    if request.method == "POST":
        answer1 = request.form["q1"]
        answer2 = request.form["q2"]
        answer3 = request.form["q3"]
        answer4 = request.form["q4"]

        session["interview_status"] = "Completed"

        return render_template(
            "interview_result.html",
            answer1=answer1,
            answer2=answer2,
            answer3=answer3,
            answer4=answer4
        )

    return render_template("interview.html")


if __name__ == "__main__":
    create_database()
    app.run(debug=True)