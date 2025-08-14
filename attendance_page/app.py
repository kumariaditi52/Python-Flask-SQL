# from flask import Flask, render_template, request, redirect, url_for, session
# import mysql.connector
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# # MySQL Connection
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="user_system"
# )
# cursor = db.cursor(dictionary=True)

# @app.route('/')
# def home():
#     return redirect(url_for('register'))

# # Register Page
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = generate_password_hash(request.form['password'])

#         try:
#             cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
#                            (name, email, password))
#             db.commit()
#             return redirect(url_for('login'))
#         except mysql.connector.Error as err:
#             if err.errno == 1062:
#                 return "Email already exists! <a href='/login'>Go to Login</a>"
#             else:
#                 return f"Error: {err}"
#     return render_template('register.html')

# # Login Page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
#         user = cursor.fetchone()

#         if user and check_password_hash(user['password'], password):
#             session['user_id'] = user['id']
#             session['name'] = user['name']
#             return redirect(url_for('dashboard'))
#         else:
#             return "Invalid email or password!"
#     return render_template('login.html')

# # Dashboard
# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' in session:
#         return render_template('dashboard.html', name=session['name'])
#     return redirect(url_for('login'))




# @app.route("/")
# def dashboard():
#     return render_template("dashboard.html")

# @app.route("/teacher")
# def teacher_dashboard():
#     return render_template("teacher_dashboard.html")

# @app.route("/student")
# def student_dashboard():
#     return render_template("student_dashboard.html")
# # Logout
# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="user_system"
)
cursor = db.cursor(dictionary=True)

# Home redirects to Register
@app.route('/')
def home():
    return redirect(url_for('register'))

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            db.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            if err.errno == 1062:
                return "Email already exists! <a href='/login'>Go to Login</a>"
            else:
                return f"Error: {err}"
    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password!"
    return render_template('login.html')

# Main Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', name=session['name'])
    return redirect(url_for('login'))

# Teacher Dashboard
@app.route("/teacher_dashboard")
def teacher_dashboard():
    if 'user_id' in session:
        return render_template("teacher_dashboard.html", name=session['name'])
    return redirect(url_for('login'))

# Student Dashboard
@app.route("/student_dashboard")
def student_dashboard():
    if 'user_id' in session:
        return render_template("student_dashboard.html", name=session['name'])
    return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
