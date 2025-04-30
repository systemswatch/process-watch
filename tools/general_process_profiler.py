#!/usr/bin/env python3

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

# Reset Screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Identify Process By Name Return PID
def find_pid_by_name(name):
    try:
        with subprocess.Popen(['pgrep', '-f', name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as all_pids:
            output, errors = all_pids.communicate()
            if errors:
                print(f"Errors:\n{errors.decode()}")
                return None
            all_pids_array = output.strip().split("\n")
            first_pid = all_pids_array[0]
            return first_pid
    except Exception as e:
        print(f"{BLACK}{BACKGROUND_BRIGHT_MAGENTA}\nAn error occurred: {e}{RESET}")
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

# General Process Profiler Menu
def general_process_profiler():
    print(f"\n{BRIGHT_GREEN}GENERAL PROCESS PROFILER SETTINGS:{RESET}")
    filename = input(f"\n{BRIGHT_CYAN}Enter the name of the configuration file:{RESET}\n")
    sanitized_filename = filename.replace(".", "-")
    process_name = input(f"\n{BRIGHT_CYAN}Enter the process name to monitor:{RESET}\n")
    while True:
        try:
            interval = int(input(f"\n{BRIGHT_CYAN}Enter the monitoring interval in seconds:{RESET}\n"))
            break
        except ValueError:
            print(f"{BLACK}{BACKGROUND_BRIGHT_MAGENTA}\nInvalid input. Please enter a number of seconds.{RESET}")
    template = f"""
    # General Process Profiler
    import os
    import sys
    import time
    import logging
    import threading
    import psutil
    import subprocess

    general_process_profiler_file = (f"{{str(os.getcwd())}}/logs/{sanitized_filename}-general-profile.log")
    error_file = (f"{{str(os.getcwd())}}/logs/error.log")

    def find_pid_by_name(name):
        try:
            with subprocess.Popen(['pgrep', '-f', name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as all_pids:
                output, errors = all_pids.communicate()
                if errors:
                    logging.error(f"Errors:\\n{{errors.decode()}}")
                    return None
                all_pids_array = output.strip().split("\\n")
                first_pid = all_pids_array[0]
                return first_pid
        except Exception as e:
            logging.error("An error occurred in Process Watch: %s", e, exc_info=True)
            raise sys.exit(1)
            return None

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
                with open(general_process_profiler_file, "a", encoding="utf-8") as f:
                    f.write(f"{process_name} running at local time {{time.ctime()}} PID: {{int(find_pid_by_name('{process_name}'))}}, Memory: {{find_memory_usage_by_pid(int(find_pid_by_name('{process_name}')))}}MB, CPU: {{find_cpu_usage_by_pid(int(find_pid_by_name('{process_name}')))}}%\\n")
                time.sleep({interval})
            except Exception as e:
                print(f"An error occurred in Process Watch configuration file {sanitized_filename}: {{e}}")
                with open(error_file, "a", encoding="utf-8") as file:
                    file.write(str(e) + (f" in {sanitized_filename}") + "\\n")
                    raise sys.exit(1)

    def worker():
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.start()

    worker()
    """
    # Write the template into a config
    write_to_file(os.path.abspath(f"../watch_list/{sanitized_filename}.py"), textwrap.dedent(template))
