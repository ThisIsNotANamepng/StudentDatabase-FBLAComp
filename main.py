from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3 

app = Flask(__name__)
app.secret_key = b'm#HS3ZyNqPNj$sga7QJVd66d!TjT6Kzr'
connection = sqlite3.connect("database.db")


@app.route('/')
def index():
  if 'username' in session: #If type is viewer or uploader, redirect to the right page, connect to databse to check if password is correct
    return f'Logged in as {session["username"]}'
  return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(l):
  return render_template("404.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
  if 'username' in session:
    return redirect(url_for('index'))
  if request.method == 'POST':
    session['username'] = request.form['username']
    session['password'] = request.form['password']
    return redirect(url_for('index'))
  return render_template('login.html')

@app.route('/logout')
def logout():
  # remove the username from the session if it's there
  session.pop('username', None)
  session.pop('password', None)
  return redirect(url_for('index')) #Add an alert that pops up when you log out
@app.route('/scan')
def scanner():
  return('This is where a scanner page would be')
@app.route('/view')
def viewer():
  return render_template('view.html')

@app.route('/admin')
def admin():
  return render_template('admin.html')




app.run(host='0.0.0.0', port=81)


