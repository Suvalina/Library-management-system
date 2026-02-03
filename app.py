from flask import Flask, render_template, request, redirect, session
import mysql.connector
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = "library_secret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="library_db"
)
cursor = db.cursor(dictionary=True)

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",(u,p))
        user = cursor.fetchone()
        if user:
            session['role'] = user['role']
            return redirect('/home')
    return render_template('login.html')

# ---------------- HOME ----------------
@app.route('/home')
def home():
    if session['role'] == 'admin':
        return render_template('admin_home.html')
    return render_template('user_home.html')

# ---------------- ADD BOOK ----------------
@app.route('/add_book', methods=['GET','POST'])
def add_book():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        category = request.form['category']
        date_p = request.form['date']
        cursor.execute(
            "INSERT INTO books(name,author,category,status,procurement_date) VALUES(%s,%s,%s,'Available',%s)",
            (name,author,category,date_p)
        )
        db.commit()
        return redirect('/home')
    return render_template('add_book.html')

# ---------------- ISSUE BOOK ----------------
@app.route('/issue_book', methods=['GET','POST'])
def issue_book():
    cursor.execute("SELECT * FROM books WHERE status='Available'")
    books = cursor.fetchall()

    if request.method == 'POST':
        serial = request.form['serial']
        mem = request.form['membership']
        issue = date.today()
        ret = issue + timedelta(days=15)

        cursor.execute(
            "INSERT INTO transactions(serial_no,membership_id,issue_date,return_date,status,fine) VALUES(%s,%s,%s,%s,'Issued',0)",
            (serial,mem,issue,ret)
        )
        cursor.execute("UPDATE books SET status='Unavailable' WHERE serial_no=%s",(serial,))
        db.commit()
        return redirect('/home')

    return render_template('issue_book.html', books=books)

# ---------------- RETURN BOOK ----------------
@app.route('/return_book', methods=['GET','POST'])
def return_book():
    if request.method == 'POST':
        tid = request.form['tid']
        actual = date.today()

        cursor.execute("SELECT * FROM transactions WHERE id=%s",(tid,))
        t = cursor.fetchone()

        fine = max(0, (actual - t['return_date']).days * 10)

        cursor.execute(
            "UPDATE transactions SET actual_return_date=%s,fine=%s,status='Returned' WHERE id=%s",
            (actual,fine,tid)
        )
        cursor.execute("UPDATE books SET status='Available' WHERE serial_no=%s",(t['serial_no'],))
        db.commit()
        return redirect('/pay_fine')

    cursor.execute("SELECT * FROM transactions WHERE status='Issued'")
    trans = cursor.fetchall()
    return render_template('return_book.html', trans=trans)

# ---------------- PAY FINE ----------------
@app.route('/pay_fine', methods=['GET','POST'])
def pay_fine():
    cursor.execute("SELECT * FROM transactions WHERE fine>0")
    fines = cursor.fetchall()

    if request.method == 'POST':
        return redirect('/home')

    return render_template('pay_fine.html', fines=fines)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
