import subprocess

# Find the process IDs (PIDs) of the server script
p1 = subprocess.Popen(['pgrep', '-f', 'main.py'], stdout=subprocess.PIPE)
output = p1.communicate()[0]
pids = output.decode().strip().split('\n')

for pid in pids:
    subprocess.run(['kill', pid])
