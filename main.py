from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as pyo

# We need a utility for uploading an existing student name to id database for use?
#https://dash.plotly.com/

#  python3.11 -m venv fbla
#  source env/bin/activate
app = Flask(__name__)
app.secret_key = b'm#HS3ZyNqPNj$sga7QJVd66d!TjT6Kzr'


def active_event():
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  thing = (cursor.execute("SELECT active_event FROM active_event").fetchall())[0][0]
  connection.close()
  return (thing)
  
    


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
  return("Well this is embarrassing, something went wrong internally")
  #Log this in a log where the admins can read it


@app.route('/login', methods=['GET', 'POST'])
def login():

  if 'username' in session:

    print(session)
    if (session['type'] == "admin"):
      return redirect(url_for('admin'))
    elif (session['type'] == "viewer"):
      return redirect(url_for('view'))
    elif (session['type'] == "uploader"):
      return redirect(url_for('upload'))
    else:
      return redirect(url_for('error'))
  
  

  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
  
    # Refresh if account doesn't exist
    if len(cursor.execute("SELECT username FROM auth WHERE lower(username) = ?", (username.lower(),)).fetchall()) == 0:
      return redirect('/login?error=invalid')
      
    #Data from the database is seperated with underline
    saved_hash = cursor.execute("SELECT hash FROM auth WHERE lower(username) = ?", (username.lower(),)).fetchall()[0][0]
    saved_username = cursor.execute("SELECT username FROM auth WHERE lower(username) = ?", (username.lower(),)).fetchall()[0][0]
    account_type = cursor.execute("SELECT type FROM auth WHERE lower(username) = ?", (username.lower(),)).fetchall()[0][0]
    connection.close()
    

    if saved_hash == password:
      session['username'] = username
      session['password'] = password
      session['type'] = account_type
      print(session)
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
      # If the username and password are incorrect, redirect to the login page
      return redirect('/login?error=invalid')

    return redirect(url_for('error'))
  return render_template('login.html')

@app.route('/admin')
def admin():
  print(session)
  if (session['type'] == "viewer"):
    return redirect(url_for('view'))
  elif (session['type'] == "uploader"):
    return redirect(url_for('upload'))
  return render_template('admin.html')
  
@app.route('/events')
def events():
  
  if (session['type'] == "uploader"):
    return redirect(url_for('upload'))
  print("Get a list of past events, choose an active event, create a new event")

  return render_template('events.html')


@app.route('/report')
def view():

  print(session)
  if (session['type'] == "uploader"):
    return redirect(url_for('upload'))

  """
  #x=events, y=number in attendance
  fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
  fig.write_html('templates/view.html')
  """

  conn = sqlite3.connect('database.db')

  cursor = conn.execute("SELECT * FROM '2-22-2023-1';")

  data = cursor.fetchall()
  x_data = [row[0] for row in data]

  # Plot the data using Plotly
  trace = go.Scatter(x=x_data, y=y_data, mode='markers')
  data = [trace]
  layout = go.Layout(title='My Plot')
  fig = go.Figure(data=data, layout=layout)
  pyo.plot(fig, filename='templates/view.html')
    
  return render_template('view.html')



  

@app.route('/scan', methods=['GET'])
def upload():

  if 'username' not in session:
    return redirect(url_for('login'))
  if (session['type'] == "viewer"):
    return redirect(url_for('view'))

  id = request.args.get('id')
  print(id)
  if id!= "None":

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

  
    big_list = (cursor.execute("SELECT ID FROM IDs WHERE ID = ?", (id,)).fetchall())
    print("Big list:", big_list)

    event_list = (cursor.execute("SELECT ID FROM '"+active_event()+"' WHERE ID = ?", (id,)).fetchall())
    print("Event list:", event_list)
    #DELETE FROM '2-22-2023-1' WHERE id='56599';
    
    id_list=[]
    for i in big_list:
      id_list.append(str(i[0]))



    




    
    if id in id_list:
      print("In ID list")
    else:
      print("Couldn't find in ID list, return error to the client")
      
    
    if id in event_list:
      print("In event list. Return 'Student already registered for this event'")
    else:
      print("Couldn't find in event list")

    if id in id_list and id not in event_list:
      print("============Entering ID=============")
      #Need to add names as well as IDs, error?
      cursor.execute("insert into '"+active_event()+"' values(?);", (id,))

      print("=====Selecting all=====")
      print(cursor.execute("select * from '2-22-2023-1';").fetchall())
      print("insert into '"+active_event()+"' values(?);", (id,))


      event_list = (cursor.execute("SELECT ID FROM '"+active_event()+"' WHERE ID = ?", (id,)).fetchall())
      print(event_list)
      print(active_event())

      
    print("====After def====")  
    print(cursor.execute("select * from '2-22-2023-1';").fetchall())

    connection.close()
    print("Insert into table")
  return render_template('scan.html')



@app.route('/logout')
def logout():
  # remove the username from the session if it's there
  session.pop('username', None)
  session.pop('password', None)
  session.pop('type', None)

  return redirect(url_for('index')) #Add an alert that pops up when you log out





app.run(host='0.0.0.0', port=5001)


