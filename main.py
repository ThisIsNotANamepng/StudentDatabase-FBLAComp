from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash
import random
import itertools

# We need a utility for uploading an existing student name to id database for use?

#  python3.11 -m venv fbla
#  source env/bin/activate
app = Flask(__name__)
app.secret_key = b'm#HS3ZyNqPNj$sga7QJVd66d!TjT6Kzr'

def change_active_event(new_event):
  new_event="'"+new_event+"'"
  print(new_event)
  #Changes the current events that the scanner page enters into
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()

  cursor.execute("DELETE FROM active_event WHERE del = 1;")
  cursor.execute(("INSERT INTO active_event(active_event,del) VALUES(?,1);"), (new_event,))

  connection.commit()
  connection.close()
  return ("Active event replaced")
def active_event():
  #Returns the current events that the scanner page enters into
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  thing = (cursor.execute("SELECT active_event FROM active_event").fetchall())[0][0]
  connection.close()
  return (thing)
def num_events():
  #Returns the number of events
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=(cursor.execute("SELECT COUNT(event) FROM event_list").fetchone()[0])
  connection.close()
  return(a)
def top_earner():
  #Returns the student with the most points
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=(cursor.execute("SELECT * FROM IDs WHERE points = (SELECT MAX(points) FROM IDs LIMIT 3)").fetchone())
  connection.close()
  return(a)
def top_three_earners():
  #Returns the top three earners
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()

  a=(cursor.execute("SELECT * FROM IDs ORDER BY points DESC LIMIT 3").fetchall())
  connection.close()
  return(a)
def random_winner():
  #Returns a random student in the ID table
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=(cursor.execute("SELECT * FROM IDs ORDER BY RANDOM() LIMIT 3 OFFSET 0").fetchone())
  connection.close()
  return(a)
def list_events():
  #Returns a list of all events
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=(cursor.execute("SELECT event FROM event_list").fetchall())
  connection.close()
  i=0
  while (i<len(a)):
    a[i]=a[i][0]
    i+=1
  return(a)
def count_events():
  #Returns a list of attendance for each event
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  events = list_events()
  counts = []
  for i in events:
    a=(cursor.execute("SELECT ID FROM '"+i+"'").fetchall())
    counts.append(len(a))
  connection.close()
  return(counts)
def num_students():
  #Returns the number of students from school_details
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=(cursor.execute("SELECT number_of_students FROM school_details;").fetchone())
  connection.close()
  return(a[0])
def list_event_names():
  #Returns a list of event names
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=(cursor.execute("SELECT name FROM event_list").fetchall())
  connection.close()
  i=0
  while (i<len(a)):
    a[i]=a[i][0]
    i+=1
  return(a)
def type_attendance(type):
  #Returns a list of attendance for a type
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  #print("All counts for events for type :"+type)

  type=type.lower()
  a=(cursor.execute("SELECT event FROM event_list WHERE type = ?", (type,)).fetchall())


  i=0
  while (i<len(a)):
    a[i]=a[i][0]
    i+=1

  counts=[]
  for i in a:
    counts.append(cursor.execute("SELECT COUNT(ID) FROM '"+i+"' ;").fetchone()[0])

  connection.close()

  return(counts)
def total_type_attendance(type):
  #Returns a list of attendance for a type
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  #print("All counts for events for type :"+type)

  type=type.lower()
  a=(cursor.execute("SELECT event FROM event_list WHERE type = ?", (type,)).fetchall())


  i=0
  while (i<len(a)):
    a[i]=a[i][0]
    i+=1

  counts=0
  for i in a:
    counts+=(cursor.execute("SELECT COUNT(ID) FROM '"+i+"' ;").fetchone()[0])

  connection.close()

  return(counts)
def average_type_attendance(type):
  #Returns a list of attendance for a type
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  #print("All counts for events for type :"+type)

  type=type.lower()
  a=(cursor.execute("SELECT event FROM event_list WHERE type = ?", (type,)).fetchall())
  if a==[]:
    return(0)


  v=0
  while (v<len(a)):
    a[v]=a[v][0]
    v+=1

  counts=0
  for i in a:
    counts+=(cursor.execute("SELECT COUNT(ID) FROM '"+i+"' ;").fetchone()[0])

  connection.close()

  return(counts/v)
def types_events(type):
  #Returns a list of events which are a type
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  #print("All counts for events for type :"+type)

  type=type.lower()

  a=(cursor.execute("SELECT event FROM event_list WHERE type = ?", (type,)).fetchall())


  i=0
  while (i<len(a)):
    a[i]=a[i][0]
    i+=1
  connection.close()

  return(a)

change_active_event('3-22-2023-1')
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


@app.route('/report', methods=['GET', 'POST'])
def view():
  global population_event
  global active_type
  total = num_students()

  
  if (session['type'] == "uploader"):
    return redirect(url_for('upload'))
  

  population_event=active_event()
  active_type="rally"
  
  
  if request.method == 'POST':
    if 'event' in request.form:
      population_event = request.form['event']
    if 'type' in request.form:
      active_type = request.form['type']

  
  top_earners_names = [top_three_earners()[0][0], top_three_earners()[1][0], top_three_earners()[2][0]]
  top_earners_points = [top_three_earners()[0][3], top_three_earners()[1][3], top_three_earners()[2][3]]
  attendance = count_events()[list_events().index(population_event)]
  remaining = total-attendance

  #type_attendance = type_attendance()

  events = (list_events())
  names = (list_event_names())
  types = ["Sport", "Rally", "Musical", "Theatre", "Other"]



  #Bar chart with types of events %wise
  percentage_types=[]
  for i in types:
    percentage_types.append(average_type_attendance(i)/total)



  
  #Radar chart with types of events vs different grades


  
  return render_template('view.html', top_earners_x=top_earners_names, top_earners_y=top_earners_points, attendance_x=[attendance, remaining], events=zip(events, names), population_event=population_event, types=types, active_type=active_type, events_type_x=types_events(active_type), events_type_y=type_attendance(active_type), events_x=list_event_names(), events_y=count_events(), percentage_types_x=types, percentage_types_y=percentage_types)



@app.route('/scan', methods=['GET', 'POST'])
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





app.run(host='0.0.0.0', port=5002)


