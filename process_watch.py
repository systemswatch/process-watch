import sys
sys.dont_write_bytecode = True
sys.path.append('watch_list')
import os
import logging
import importlib


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

#if __name__ == "__main__":
