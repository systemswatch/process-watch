import os
import sys
import time
import logging
import importlib
import psutil

sys.dont_write_bytecode = True
sys.path.append('watch_list')

# Logging Configuration
os.makedirs(os.getcwd() + "/logs", exist_ok=True)
log_file = (f"{str(os.getcwd())}/logs/process_watch.log")

logging.basicConfig(
    handlers = [logging.FileHandler(log_file), logging.StreamHandler()],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Dynamic Import of Modules in Watch List Directory
def import_watch_list():
    gbl = globals()
    watch_list_directory_path = "watch_list"
    for filename in os.listdir(watch_list_directory_path):
        try:
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]  # Remove the .py extension
                gbl[module_name] = importlib.import_module(f"{module_name}")
        except Exception as e:
            logging.error("An error occurred in Process Watch: %s", e, exc_info=True)
            raise sys.exit(1)

import_watch_list()

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

#a = find_procs_by_name("diagnostics_agent")
# print(a)

# Main Logic
def processwatch():

    while True:
        try:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"Main Running at {time.ctime()}\n")
            time.sleep(10)
        except Exception as e:
            logging.error("An error occurred in Process Watch: %s", e, exc_info=True)
            raise sys.exit(1)

if __name__ == "__main__":
    print(sys.modules.keys())
    print(sys.path)
    processwatch()
