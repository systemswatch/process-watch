#!/usr/bin/env python

import os
import textwrap
import subprocess

# Menu ANSI Colors
BLACK = '\033[30m'
GREEN = '\033[32m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_YELLOW = '\033[93m'
BACKGROUND_BRIGHT_MAGENTA = '\033[105m'
RESET = '\033[0m'

# Reset Sceen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Identify Process By Name Return PID
def find_pid_by_name(name):
    try:
        with subprocess.Popen(['pgrep', '-f', name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as all_pids:
            output, errors = all_pids.communicate()
            all_pids_array = output.strip().split("\n")
            first_pid = all_pids_array[0]
        return first_pid
    except Exception as e:
        print(f"{BLACK}{BACKGROUND_BRIGHT_MAGENTA}\nAn error occurred: {errors} {e}{RESET}")
        return None

# Write configuration file to watch_list directory
def write_to_file(filename, template):
    try:
        with open(os.path.join(os.pardir, "watch_list", filename), 'w', encoding="utf-8") as file:
            file.write(template)
        clear_screen()
        print(f"\n{GREEN}'{filename}' configuration created.{RESET}")
    except Exception as e:
        print(f"{BLACK}{BACKGROUND_BRIGHT_MAGENTA}\nAn error occurred: {e}{RESET}")

# Process Profiler General Menu
def process_profiler_general():
    print(f"\n{BRIGHT_GREEN}SERVICE PROFILER GENERAL SETTINGS:{RESET}")
    filename = input(f"\n{BRIGHT_CYAN}Enter the name of the configuration file:{RESET}\n")
    sanitized_filename = filename.replace(".", "-")
    process_name = input(f"\n{BRIGHT_CYAN}Enter the process name to monitor:{RESET}\n")
    process_id = int(find_pid_by_name(process_name))
    interval = input(f"\n{BRIGHT_CYAN}Enter the monitoring interval in seconds:{RESET}\n")
    # Service Profiler General Template
    template = f"""
    import os
    import sys
    import time
    import logging
    import threading
    import psutil
    import subprocess

    output_file = (f"{{str(os.getcwd())}}/logs/process_watch.log")

    def find_pid_by_name(name):
        try:
            with subprocess.Popen(['pgrep', '-f', name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as all_pids:
                output, errors = all_pids.communicate()
                all_pids_array = output.strip().split("\\n")
                first_pid = all_pids_array[0]
            return first_pid
        except Exception as e:
            logging.error("An error occurred in Process Watch: %s", e, exc_info=True)
            raise sys.exit(1)

    process_id = int(find_pid_by_name("{process_name}"))

    def find_memory_usage_by_pid(pid):
        process = psutil.Process(pid)
        memory_info = process.memory_info()
        rss_bytes = memory_info.rss
        rss_megabytes = int(rss_bytes / (1024 * 1024))
        if rss_megabytes:
            return rss_megabytes
        else:
            return ("Process N/A.")

    def find_cpu_usage_by_pid(pid):
        process = psutil.Process(pid)
        cpu_percentage = process.cpu_percent(interval=1)
        if cpu_percentage:
            return cpu_percentage
        else:
            return ("0.0")

    def monitor():

        while True:
            try:
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"{process_name} running at local time {{time.ctime()}} PID: {process_id}, Memory: {{find_memory_usage_by_pid({process_id})}}MB, CPU: {{find_cpu_usage_by_pid({process_id})}}%\\n")
                time.sleep({interval})
            except Exception as e:
                logging.error("An error occurred in Process Watch: %s", e, exc_info=True)
                raise sys.exit(1)

    def worker():
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.start()

    worker()
    """
    # Write the template into a  config
    write_to_file(os.path.abspath(f"../watch_list/{sanitized_filename}.py"), textwrap.dedent(template))
