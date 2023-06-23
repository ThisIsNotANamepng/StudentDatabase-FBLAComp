import requests
import sqlite3
import socket
import shutil




#Check if the server is up
def is_responding(ip_address):
    try:
        response = requests.get(f"http://{ip_address}:5005/diagnostics")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

hostname = socket.gethostname()
def get_server_ip(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        return None
ip = get_server_ip(hostname)

if is_responding(ip):
    print(f"The IP address {ip} is responding                       [🗸]")
else:
    print(f"The IP address {ip} is not responding                   [x]")




#Open and close database
try:
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    a=(cursor.execute("SELECT * FROM school_details;").fetchone())

    connection.close()
    print("Database is unlocked and working                             [🗸]")
except:
    print("Database is either locked, broken, or in the wrong location  [x]")


#Check available disk space
total, used, free = shutil.disk_usage(".")

# Use the free_space variable for further processing
# For example:
if free > (1024 ** 3):
    print("There is at least 1 GB of disk space                         [🗸]")
else:
    print("There is less than 1 GB of disk space                        [x]")
