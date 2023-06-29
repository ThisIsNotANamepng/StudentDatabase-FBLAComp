import threading
import os
import time
import hashlib
import sqlite3 
import subprocess


def sync_with_rsync(password):
    rsync_command = ['rsync', '-az', 'database.db', 'jjhags@100.115.92.204:~/backuplocation/database.db']
    
    # Start the rsync process and capture the output
    rsync_process = subprocess.Popen(rsync_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Pass the password to rsync through stdin
    rsync_output, rsync_error = rsync_process.communicate(input=password.encode())
    
    # Decode and print the output
    print(rsync_output.decode())
    
    # Check for any errors
    if rsync_error:
        print("Error:", rsync_error.decode())
    
    # Wait for the process to finish
    rsync_process.wait()

# Usage
password = 'bigpassword'
sync_with_rsync(password)

