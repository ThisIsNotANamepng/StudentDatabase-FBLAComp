import subprocess
import time

print("Starting server...")
process = subprocess.Popen(['nohup', 'fbla/bin/python3', 'main.py'])

time.sleep(4)
f=open("ip.txt", "r")
print("Server started at "+f.read())
f.close()