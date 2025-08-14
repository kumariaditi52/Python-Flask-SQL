from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="booking_db"
    )

@app.route('/')
def home():
    return render_template('booking.html')

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (name, email, date, time) VALUES (%s, %s, %s, %s)",
        (name, email, date, time)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('bookings_list'))

# Show all bookings + search
@app.route('/bookings', methods=['GET', 'POST'])
def bookings_list():
    conn = get_connection()
    cursor = conn.cursor()

    # Update booking if form submitted
    if request.method == 'POST' and 'id' in request.form:
        booking_id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        cursor.execute(
            "UPDATE bookings SET name=%s, email=%s, date=%s, time=%s WHERE id=%s",
            (name, email, date, time, booking_id)
        )
        conn.commit()

    # Search functionality
    search_query = request.args.get('search', '')
    if search_query:
        cursor.execute(
            "SELECT * FROM bookings WHERE name LIKE %s OR email LIKE %s",
            (f"%{search_query}%", f"%{search_query}%")
        )
    else:
        cursor.execute("SELECT * FROM bookings")
    
    bookings = cursor.fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings, search_query=search_query)

# Delete booking
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('bookings_list'))

if __name__ == '__main__':
    app.run(debug=True)
