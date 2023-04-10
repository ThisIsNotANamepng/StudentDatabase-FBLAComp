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
def randomm_winner():
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
def count_events_grade(grade):
  #Returns a list of attendance for each event according to the inputted grade
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  events = list_events()
  counts = []
  for i in events:
    count=0
    a=(cursor.execute("SELECT ID FROM '"+i+"'").fetchall())
    #print("a", a)
    for i in a:
      #i = an id
      b=(cursor.execute("SELECT grade FROM IDs WHERE ID = ?", (i[0],)).fetchall())
      if len(b)!=0:
        if int(b[0][0])==grade:
          count+=1
    counts.append(count)

  connection.close()
  return(counts)
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
def randomm_winner_each_grade():
  #Returns a list of winners from each grade in the order of [grade9name, 9id, grade10name, 10id...
  #Returns a random student in the ID table
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=[]
  a.append(cursor.execute("SELECT name FROM IDs WHERE grade = 9 ORDER BY RANDOM() LIMIT 1;").fetchone()[0])
  a.append(cursor.execute("SELECT ID FROM IDs WHERE grade = 9 ORDER BY RANDOM() LIMIT 1;").fetchone()[0])
  a.append(cursor.execute("SELECT name FROM IDs WHERE grade = 10 ORDER BY RANDOM() LIMIT 1;").fetchone()[0])
  a.append(cursor.execute("SELECT ID FROM IDs WHERE grade = 10 ORDER BY RANDOM() LIMIT 1;").fetchone()[0])
  a.append(cursor.execute("SELECT name FROM IDs WHERE grade = 11 ORDER BY RANDOM() LIMIT 1;").fetchone()[0])
  a.append(cursor.execute("SELECT ID FROM IDs WHERE grade = 11 ORDER BY RANDOM() LIMIT 1;").fetchone()[0])
  a.append(cursor.execute("SELECT name FROM IDs WHERE grade = 12 ORDER BY RANDOM() LIMIT 1;").fetchone()[0])
  a.append(cursor.execute("SELECT ID FROM IDs WHERE grade = 12 ORDER BY RANDOM() LIMIT 1;").fetchone()[0])


  connection.close()
  return(a)
def grade_points():
  #Returns a list of the points each grade has in the order of [9, 10, 11, 12]
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=[]
  a.append(cursor.execute("SELECT SUM(points) FROM IDs WHERE grade = 9;").fetchone()[0])
  a.append(cursor.execute("SELECT SUM(points) FROM IDs WHERE grade=10;").fetchone()[0])
  a.append(cursor.execute("SELECT SUM(points) FROM IDs WHERE grade=11;").fetchone()[0])
  a.append(cursor.execute("SELECT SUM(points) FROM IDs WHERE grade=12;").fetchone()[0])

  connection.close()
  return(a)
def student_names():
  #Returns a list of all of the student names
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=(cursor.execute("SELECT name FROM IDs").fetchall())
  connection.close()
  i=0
  while (i<len(a)):
    a[i]=a[i][0]
    i+=1
  return(a)
def student_points():
  #Returns a list of all of the student names
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=(cursor.execute("SELECT points FROM IDs").fetchall())
  connection.close()
  i=0
  while (i<len(a)):
    a[i]=a[i][0]
    i+=1
  return(a)
def reset_students():
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  cursor.execute('UPDATE IDs SET points = 0')
  connection.commit()
  connection.close()
def all_usernames():
  #Returns a list of all of the student names
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=(cursor.execute("SELECT username FROM auth").fetchall())
  connection.close()
  i=0
  while (i<len(a)):
    a[i]=a[i][0]
    i+=1
  return(a)


@app.route('/')
def index():
  if 'type' in session:
    if (session['type'] == "admin"):
      return redirect(url_for('admin'))
    elif (session['type'] == "viewer"):
      return redirect(url_for('view'))
    elif (session['type'] == "uploader"):
      return redirect(url_for('upload'))
    else:
      return redirect(url_for('error'))
  else:
    return redirect(url_for('login'))
  
@app.errorhandler(404)
def not_found(l):
  return render_template("404.html")
  #Return to log in?

@app.route('/error')
def error():
  return("Well this is embarrassing, something went wrong internally")
  #Log this in a log where the admins can read it

@app.route('/help')
def help():
  return(render_template('help.html'))

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
  if (session['type'] == "viewer"):
    return redirect(url_for('view'))
  elif (session['type'] == "uploader"):
    return redirect(url_for('upload'))


  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  cursor.execute('SELECT * FROM auth')
  accounts = cursor.fetchall()
  connection.close()

  if request.method == 'POST':
    usernames=all_usernames()
    print(request.form)
    if request.form.get("user_to_change") != None:
      connection = sqlite3.connect("database.db")
      cursor = connection.cursor()

      print("UPDATE auth SET password = ? WHERE username="+request.form.get('user_to_change')+";")
      cursor.execute("UPDATE auth SET hash = ? WHERE username='"+request.form.get('user_to_change')+"';", (request.form.get("new_password"),))

      



      connection.commit()
      connection.close()
    if request.form.get('regenerate_points') == 'regenerate_points':
      # Sets all student points to zero
      reset_students()
    if request.form.get('username') != None:
      #Create new user
      newuser_username = request.form['username']
      newuser_password = request.form['password']
      newuser_type = request.form['type']

      connection = sqlite3.connect("database.db")
      cursor = connection.cursor()
      cursor.execute("INSERT INTO auth (username, hash, type) VALUES ('"+newuser_username+"', '"+newuser_password+"', '"+newuser_type+"');")
      connection.commit()
      connection.close()
    for i in usernames:
      if 'delete_user_'+i in request.form:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('DELETE FROM auth WHERE username=?', (i,))
        connection.commit()
        connection.close()

       





  return render_template('admin.html', accounts=accounts, users=all_usernames())
  
@app.route('/events')
def events():
  
  if (session['type'] == "uploader"):
    return redirect(url_for('upload'))
  print("Get a list of past events, choose an active event, create a new event")

  return render_template('events.html')

@app.route('/report', methods=['GET', 'POST'])
def view():


  if 'type' in session:
    if (session['type'] == "admin"):
      pass
    elif (session['type'] == "viewer"):
      pass
    elif (session['type'] == "uploader"):
      return redirect(url_for('upload'))
    else:
      return redirect(url_for('error'))
  else:
    return redirect(url_for('login'))

  
  global population_event
  global active_type
  global active_grade
  total = num_students()

  
  if (session['type'] == "uploader"):
    return redirect(url_for('upload'))
  

  population_event=active_event()
  active_type="rally"
  active_grade=12
  
  
  
  if request.method == 'POST':
    if 'event' in request.form:
      population_event = request.form['event']
    if 'type' in request.form:
      active_type = request.form['type']
    if 'grade' in request.form:
      active_grade = request.form['grade']   


  
  top_earners_names = [top_three_earners()[0][0], top_three_earners()[1][0], top_three_earners()[2][0]]
  top_earners_points = [top_three_earners()[0][3], top_three_earners()[1][3], top_three_earners()[2][3]]


  if "'" in population_event:
    population_event=population_event[1:-1]

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

  #Bar chart to display each event with a dropdown menu to change the grade which is displayed (by number of attendance)
  grades=[9, 10, 11, 12]


  
  #Radar chart with types of events vs different grades


  
  return render_template('view.html', top_earners_x=top_earners_names, top_earners_y=top_earners_points, attendance_x=[attendance, remaining], events=zip(events, names), population_event=population_event, types=types, active_type=active_type, events_type_x=types_events(active_type), events_type_y=type_attendance(active_type), events_x=list_event_names(), events_y=count_events(), percentage_types_x=types, percentage_types_y=percentage_types, grade_events_list_x=list_event_names(), grade_events_list_y=count_events_grade(active_grade), grade_events_list_grade=active_grade, grades=grades, active_grade=active_grade, grade_points_y=grade_points(), grade_points_data=grade_points(), student_points=student_points(), student_names=student_names())

@app.route('/winners', methods=['GET', 'POST'])
def winner():
  global student
  global random_winner
  global random_winner_each_grade

  #The page where viewers can pick winners

  #Pick a winner for each grade
  #Search for students to get their points (and which events they attended?)
  #Ability to add a student to an event
  random_winner=""
  random_winner_each_grade=""
  results=""

  if request.method == 'POST':
    if request.form.get('generate_student') == 'generate_student':
      # Pass the single student
      random_winner=randomm_winner()
    elif  request.form.get('generate_students') == 'generate_students':
      # Pass the students
      random_winner_each_grade=randomm_winner_each_grade()      


  if 'query' in request.form:
    query = request.form['query']
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM IDs WHERE name LIKE ?', ('%' + query + '%',))
    results = cursor.fetchall()
    connection.close()

  return render_template('winners.html', results=results, single_winner=random_winner, all_winners=random_winner_each_grade)

@app.route('/scan', methods=['GET', 'POST'])
def upload():

  if 'username' not in session:
    return redirect(url_for('login'))
  if (session['type'] == "viewer"):
    return redirect(url_for('view'))

  id = request.args.get('id')

  if id != "None":

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("insert into "+active_event()+" values(?);", (id,))
    cursor.execute("UPDATE IDs SET points = points + 1 WHERE id = ?;", (id,))
    connection.commit()
    connection.close()

  return render_template('scan.html')

@app.route('/logout')
def logout():
  # remove the username from the session if it's there
  session.pop('username', None)
  session.pop('password', None)
  session.pop('type', None)

  return redirect(url_for('index')) #Add an alert that pops up when you log out





app.run(host='0.0.0.0', port=5002)


