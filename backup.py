import threading
import os
import time
import hashlib

# Infinite loop to check file and backup when nessecary
# Rsync only transfers the difference between files, it's an incremental backup
# - Get hash of database.db

while True:
    # - Hash database.db
    if newhash!=hash:
        hash=newhash
        # - Read rsync destinations from database.db
        for destination in destinations:
            os.system("rsync "+destination)