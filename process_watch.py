#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
sys.path.append('watch_list')
import os
import logging
import importlib

# Logging Configuration
os.makedirs(os.getcwd() + "/logs", exist_ok=True)
log_file = (f"{str(os.getcwd())}/logs/process_watch.log")
error_file = (f"{str(os.getcwd())}/logs/error.log")

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
            print(f"An error occurred in Process Watch: {e}")
            with open(error_file, "a", encoding="utf-8") as file:
                file.write(str(e) + "\n")
                raise sys.exit(1)

import_watch_list()
