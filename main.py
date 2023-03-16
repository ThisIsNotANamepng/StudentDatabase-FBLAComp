from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = b'm#HS3ZyNqPNj$sga7QJVd66d!TjT6Kzr'



@app.route('/')
def index():
  """
  if (session['type'] == "admin"):
    return redirect(url_for('admin'))
  elif (session['type'] == "viewer"):
    return redirect(url_for('view'))
  elif (session['type'] == "uploader"):
    return redirect(url_for('upload'))
  else:
    return redirect(url_for('error'))
  """
  return redirect(url_for('login'))
  

@app.errorhandler(404)
def not_found(l):
  return render_template("404.html")

@app.route('/error')
def error():
  return render("Well this is embarrassing, something went wrong internally")


@app.route('/login', methods=['GET', 'POST'])
def login():

  if 'username' in session:
    return redirect(url_for('index'))
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
  
    # Refresh if account doesn't exist
    if len(cursor.execute("SELECT username FROM auth WHERE lower(username) = ?", (username.lower(),)).fetchall()) == 0:
      return redirect('/login?error=exist')
      
    #Data from the database is seperated with underline
    saved_hash = cursor.execute("SELECT hash FROM auth WHERE lower(username) = ?", (username.lower(),)).fetchall()[0][0]
    saved_username = cursor.execute("SELECT username FROM auth WHERE lower(username) = ?", (username.lower(),)).fetchall()[0][0]
    account_type = cursor.execute("SELECT type FROM auth WHERE lower(username) = ?", (username.lower(),)).fetchall()[0][0]
    

    if saved_hash == password:#DO THINGS HERE
      connection.close()
      session['username'] = username
      session['password'] = password
      session['type'] = account_type
      if (session['type'] == "admin"):
        return redirect(url_for('admin'))
      elif (session['type'] == "viewer"):
        return redirect(url_for('view'))
      elif (session['type'] == "uploader"):
        return redirect(url_for('upload'))
      else:
        return redirect(url_for('error'))
      # Redirect to the main page
      return redirect('/')
    else:
      # Close database connection
      connection.close()
      # If the username and password are incorrect, redirect to the login page
      return redirect('/login?error=invalid')

    return redirect(url_for('error'))
  return render_template('login.html')

@app.route('/admin')
def admin():
  return render_template('admin.html')
  
@app.route('/report')
def view():
  return render_template('view.html')

@app.route('/scan')
def upload():
  return render_template('scan.html')



@app.route('/logout')
def logout():
  # remove the username from the session if it's there
  session.pop('username', None)
  session.pop('password', None)
  session.pop('type', None)

  return redirect(url_for('index')) #Add an alert that pops up when you log out





app.run(host='0.0.0.0', port=81)


