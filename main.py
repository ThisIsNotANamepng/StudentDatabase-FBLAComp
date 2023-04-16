from flask import Flask, render_template, session, request, redirect, url_for, send_from_directory
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash
import random
import itertools
import datetime 
import time

#  python3.11 -m venv fbla
#  source env/bin/activate
app = Flask(__name__)
app.secret_key = b'm#HS3Zy57d$^&fvNqPNj$sga7QJ^*fd66d!TjT6Kzr'
def log(to_log):
  to_log="\n"+str(datetime.datetime.now())+" - "+to_log

  f=open("log.txt", "a")
  f.write(to_log)
  f.close()
def does_event_exist(id):
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()

  a=(cursor.execute("SELECT * FROM event_list WHERE event = '"+str(id)+"';").fetchone())
  
  connection.close()

  if a==None:
    return(False)#Maybe does the id append notmiterate up
  return(True)
def change_active_event(new_event):
  new_event="'"+new_event+"'"
  #Changes the current events that the scanner page enters into
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()

  cursor.execute("DELETE FROM active_event WHERE del = 1;")#del = 1 becasue I made a simple column to find which event to delete, I could just use delete *
  cursor.execute(("INSERT INTO active_event(active_event,del) VALUES(?,1);"), (new_event,))

  connection.commit()
  connection.close()
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
def new_event(name, type):
  #Inserts a new event into the database. Take the name and type and creates a unique ID
  date=datetime.datetime.now().strftime('%m-%d-%Y')

  a=True
  i=1
  while(a==True):
    append="-"+str(i)
    if does_event_exist(date+append)==True:  
      i+=1
    else:
      date=str(date)
      append=(str(append))
      new_event_id=(str(date)+str(append))

      connection = sqlite3.connect("database.db")
      cursor = connection.cursor()

      cursor.execute("INSERT INTO event_list(event,type,name) VALUES('"+new_event_id+"','"+type+"','"+name+"');")
      cursor.execute("CREATE TABLE '"+new_event_id+"'(ID text);")

      connection.commit()
      connection.close()

      a=False
    if (i>1000):
      print("Loop broken. Exiting")
      a=False
def delete_event(event):
      connection = sqlite3.connect("database.db")
      cursor = connection.cursor()
      cursor.execute("DROP TABLE '"+event+"';")
      cursor.execute("DELETE FROM event_list WHERE event='"+event+"';")
      connection.commit()
      connection.close()
def return_all_students():
  #Returns the number of students from school_details
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  a=(cursor.execute("SELECT * FROM IDs;").fetchall())
  connection.close()

  return(a)

@app.route('/favicon.ico')
def favicon():
  return url_for(filename='favicon.ico')

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
      log(username+" logged in")
      session['password'] = password
      session['type'] = account_type
      if (session['type'] == "admin"):
        log(username+" logged in as "+account_type)
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

global admin_jinja_message
global admin_jinja_message_2
global admin_toggle_message

admin_jinja_message=""
admin_jinja_message_2=""
admin_toggle_message=False

@app.route('/admin', methods=['GET', 'POST'])
def admin():
  global admin_jinja_message
  global admin_jinja_message_2
  global admin_toggle_message

  if admin_toggle_message==False:
    admin_jinja_message=""
    admin_jinja_message_2=""
  else:
    admin_toggle_message=False 

  if 'username' in session:
    if (session['type'] == "admin"):
      pass
    elif (session['type'] == "viewer"):
      return redirect(url_for('view'))
    elif (session['type'] == "uploader"):
      return redirect(url_for('upload'))
    else:
      return redirect(url_for('error'))
  else:
    return redirect(url_for('login'))

  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  cursor.execute('SELECT * FROM auth')
  accounts = cursor.fetchall()
  connection.close()

  if request.method == 'POST':
    usernames=all_usernames()
    if request.form.get("user_to_change") != None:
      #Change password for user
      log(request.form.get('user_to_change')+"'s password was changed")
      connection = sqlite3.connect("database.db")
      cursor = connection.cursor()
      cursor.execute("UPDATE auth SET hash = ? WHERE username='"+request.form.get('user_to_change')+"';", (request.form.get("new_password"),))
      connection.commit()
      connection.close()
      admin_toggle_message=True
      admin_jinja_message="changed_password"
      admin_jinja_message_2=request.form.get("user_to_change")
    if request.form.get('regenerate_points') == 'regenerate_points':
      # Sets all student points to zero
      log("All student points were reset to zero")
      reset_students()
      admin_toggle_message=True
      admin_jinja_message="reset_students"
    if request.form.get('username') != None:
      #Create new user
      newuser_username = request.form['username']
      newuser_password = request.form['password']
      newuser_type = request.form['type']
      log(newuser_username+" was created")
      connection = sqlite3.connect("database.db")
      cursor = connection.cursor()
      cursor.execute("INSERT INTO auth (username, hash, type) VALUES ('"+newuser_username+"', '"+newuser_password+"', '"+newuser_type+"');")
      connection.commit()
      connection.close()
      admin_toggle_message=True
      admin_jinja_message="created_account"
      admin_jinja_message_2=newuser_username
    for i in usernames:
      #Delete user
      if 'delete_user_'+i in request.form:
        log(i+" was deleted")
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('DELETE FROM auth WHERE username=?', (i,))
        connection.commit()
        connection.close()
        admin_toggle_message=True
        admin_jinja_message="deleted_user"
        admin_jinja_message_2=i
    return redirect(url_for('admin'))
    
  f=open("log.txt", "r")
  llog=f.readlines()
  f.close()

  return render_template('admin.html', accounts=accounts, users=all_usernames(), log=llog, jinja_message=admin_jinja_message, jinja_message_2=admin_jinja_message_2)

global events_jinja_message
global events_jinja_message_2
global events_toggle_message

events_jinja_message=""
events_jinja_message_2=""
events_toggle_message=False

@app.route('/events', methods=['GET', 'POST'])
def events():
  global events_jinja_message
  global events_jinja_message_2
  global events_toggle_message


  if events_toggle_message==False:
    events_jinja_message=""
    events_jinja_message_2=""
  else:
    events_toggle_message=False

  if 'username' in session:
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

  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  cursor.execute('SELECT * FROM event_list')
  events = cursor.fetchall()
  connection.close()
  
  types = ["Sport", "Rally", "Musical", "Theatre", "Other"]
  if request.method == 'POST':
    if 'event_type' in request.form:
      #Create a new event
      new_event_name = request.form['event_name']
      new_event_type = request.form['event_type']
      log(new_event_name+" event was created")
      new_event(new_event_name, new_event_type)
      events_toggle_message=True
      events_jinja_message="create_event"
      events_jinja_message_2=new_event_name
    elif "new_active_event" in request.form:
      #Change active event
      change_active_event(request.form['new_active_event'])
      log(request.form['new_active_event']+" was changed to the active event")
      events_toggle_message=True
      events_jinja_message="change_active_event"
      events_jinja_message_2=request.form['new_active_event']
    for i in request.form:
      #Delete event
      if "delete_event_" in i:
        to_delete=(i[13:])
        log(to_delete+" was deleted")
        delete_event(to_delete)
        events_toggle_message=True
        events_jinja_message="delete_event"
        events_jinja_message_2=to_delete
    return redirect(url_for('events'))
      




  return render_template('events.html', events=events, types=types, active_event=active_event()[1:-1], jinja_message=events_jinja_message, jinja_message_2=events_jinja_message_2, session_type=session['type'])

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

  types = ["Sport", "Rally", "Musical", "Theatre", "Other"]

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



  #Bar chart with types of events %wise
  percentage_types=[]
  for i in types:
    percentage_types.append(average_type_attendance(i)/total)

  #Bar chart to display each event with a dropdown menu to change the grade which is displayed (by number of attendance)
  grades=[9, 10, 11, 12]

  title_name=names[events.index(population_event)]
  return render_template('view.html', top_earners_x=top_earners_names, top_earners_y=top_earners_points, attendance_x=[attendance, remaining], events=zip(events, names), population_event=population_event, types=types, active_type=active_type, events_type_x=types_events(active_type), events_type_y=type_attendance(active_type), events_x=list_event_names(), events_y=count_events(), percentage_types_x=types, percentage_types_y=percentage_types, grade_events_list_x=list_event_names(), grade_events_list_y=count_events_grade(active_grade), grade_events_list_grade=active_grade, grades=grades, active_grade=int(active_grade), grade_points_y=grade_points(), grade_points_data=grade_points(), student_points=student_points(), student_names=student_names(), title_name=title_name, session_type=session['type'])

@app.route('/winners', methods=['GET', 'POST'])
def winner():

  if 'username' in session:
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
      #jinja_message="single_student"
    elif  request.form.get('generate_students') == 'generate_students':
      # Pass the students
      random_winner_each_grade=randomm_winner_each_grade()
      #jinja_message="multiple_students"

    #return redirect(url_for('winner'))   


  if 'query' in request.form:
    query = request.form['query']
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM IDs WHERE name LIKE ?', ('%' + query + '%',))
    results = cursor.fetchall()
    connection.close()

  return render_template('winners.html', results=results, single_winner=random_winner, all_winners=random_winner_each_grade, students=return_all_students(), session_type=session['type'])

@app.route('/scan', methods=['GET', 'POST'])
def upload():
  jinja_message=""

  if 'username' in session:
    if (session['type'] == "admin"):
      pass
    elif (session['type'] == "viewer"):
      return redirect(url_for('report'))
    elif (session['type'] == "uploader"):
      pass
    else:
      return redirect(url_for('error'))
  else:
    return redirect(url_for('login'))

  id = request.args.get('id')

  if id != "None":

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("insert into "+active_event()+" values(?);", (id,))
    cursor.execute("UPDATE IDs SET points = points + 1 WHERE id = ?;", (id,))
    jinja_message=cursor.execute("SELECT name FROM IDs WHERE id = ?;", (id,)).fetchone()
    connection.commit()
    connection.close()
  return render_template('scan.html', jinja_message=jinja_message, session_type=session['type'])

@app.route('/logout')
def logout():
  # remove the username from the session if it's there
  session.pop('username', None)
  session.pop('password', None)
  session.pop('type', None)

  return redirect(url_for('index')) #Add an alert that pops up when you log out

app.run(host='0.0.0.0', port=5005)