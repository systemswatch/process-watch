import os
import sys
import time
import logging
import threading
import psutil

output_file = (f"{str(os.getcwd())}/process_watch.out")

# Identify Processes By Name
def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(["name", "exe", "cmdline"]):
        if name == p.info['name'] or \
                p.info['exe'] and os.path.basename(p.info['exe']) == name or \
                p.info['cmdline'] and p.info['cmdline'][0] == name:
            ls.append(p)
    return ls

def monitor2():
    while True:
        try:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"Test 2 Running at {time.ctime()} {find_procs_by_name('diagnostics_agent')}\n")
            time.sleep(10)
        except Exception as e:
            logging.error("An error occurred in Process Watch: %s", e, exc_info=True)
            raise sys.exit(1)

def worker():
    monitor2_thread = threading.Thread(target=monitor2)
    monitor2_thread.start()

worker()
