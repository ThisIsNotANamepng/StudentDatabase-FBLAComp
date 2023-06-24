import subprocess
import time

print("Starting server...")
process = subprocess.Popen(['nohup', 'python3', '/fbla/main.py'])

time.sleep(4)
f=open("ip.txt", "r")
print("Server started at "+f.read())
f.close()