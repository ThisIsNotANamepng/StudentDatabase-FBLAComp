import threading
import os
import time
import hashlib
import sqlite3 
import subprocess

# Infinite loop to check file and backup when nessecary
# Rsync only transfers the difference between files, it's an incremental backup
# - Get hash of database.db

def hash_db():
   h = hashlib.sha256()
   with open('database.db','rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)

   return h.hexdigest()



def sync_with_rsync(password):
    rsync_command = ['rsync', '-az', '--password-file=-', 'database.db', 'jjhags@100.115.92.204:~/backuplocation/database.db']
    
    # Start the rsync process
    rsync_process = subprocess.Popen(rsync_command, stdin=subprocess.PIPE)
    
    # Pass the password to rsync through stdin
    rsync_process.communicate(input=password.encode())
    
    # Wait for the process to finish
    rsync_process.wait()

# Usage
password = 'your_password'
sync_with_rsync(password)


hash=hash_db()
while True:
    # - Hash database.db
    newhash=hash_db()
    if newhash!=hash:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        destinations = (cursor.execute("SELECT * FROM backups").fetchall())
        connection.close()

        hash=newhash
        # - Read rsync destinations from database.db
        for destination in destinations:
            os.system("rsync -az --password-file=passwordfiles/"+destination+".txt database.db "+destination)
            #rsync -avz --password-file=password.txt <source_file> <remote_user>@<remote_host>:<destination_path>
            #rsync -avz example.txt user@example.com:/path/to/destination




    time.sleep(5)