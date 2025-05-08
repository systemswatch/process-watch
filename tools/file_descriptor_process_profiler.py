#!/usr/bin/env python3

import os
import textwrap
import subprocess

# Base Directory
base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)

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

# Write configuration file to watch_list directory
def write_to_file(filename, template):
    try:
        with open(os.path.join(os.pardir, "watch_list", filename), 'w', encoding="utf-8") as file:
            file.write(template)
        clear_screen()
        print(f"\n{GREEN}'{filename}' configuration created.{RESET}")
    except Exception as e:
        print(f"{BLACK}{BACKGROUND_BRIGHT_MAGENTA}\nAn error occurred: {e}{RESET}")

# File Descriptor Process Profiler Menu
def file_descriptor_process_profiler():
    print(f"\n{BRIGHT_GREEN}FILE DESCRIPTOR PROCESS PROFILER SETTINGS:{RESET}")
    filename = input(f"\n{BRIGHT_CYAN}Enter the name of the configuration file:{RESET}\n")
    sanitized_filename = filename.replace(".", "-")
    process_name = input(f"\n{BRIGHT_CYAN}Enter the process name to monitor {GREEN}(use name in ps ouput){RESET}:{RESET}\n")
    while True:
        try:
            interval = int(input(f"\n{BRIGHT_CYAN}Enter the monitoring interval {GREEN}(in seconds){RESET}:{RESET}\n"))
            break
        except ValueError:
            print(f"{BLACK}{BACKGROUND_BRIGHT_MAGENTA}\nInvalid input. Please enter a number of seconds.{RESET}")
    while True:
        try:
            file_descriptor_threshold = int(input(f"\n{BRIGHT_CYAN}Enter the file descriptor threshold of the process:{RESET}\n"))
            break
        except ValueError:
            print(f"{BLACK}{BACKGROUND_BRIGHT_MAGENTA}\nInvalid input. Please enter the number of file descriptors.{RESET}")
    action = input(f"\n{BRIGHT_CYAN}Enter the action to take upon the file descriptor threshold being met {GREEN}(leave blank for no action){RESET}:{RESET}\n") or "echo"

    template = f"""
    # File Descriptor Process Profiler
    import os
    import sys
    import time
    import logging
    import threading
    import psutil
    import subprocess

    file_descriptor_process_profiler_file = (f"{{str(os.getcwd())}}/logs/{sanitized_filename}-fds-profiler.log")
    error_file = (f"{{str(os.getcwd())}}/logs/error.log")

    def find_pid_by_name(name):
        try:
            with subprocess.Popen(['pgrep', '-xf', name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as all_pids:
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

    def find_file_descriptor_usage_by_pid(pid):
        process = psutil.Process(pid)
        file_descriptor_usage_info = process.num_fds()
        if  file_descriptor_usage_info:
            return file_descriptor_usage_info
        else:
            return("0.0")

    def monitor():
        while True:
            try:
                process_pid = find_pid_by_name('{process_name}')
                process_file_descriptor_set = {{find_file_descriptor_usage_by_pid(int(find_pid_by_name('{process_name}')))}}
                process_file_descriptor = int(process_file_descriptor_set.pop())
                if int(process_file_descriptor) >= {file_descriptor_threshold}:
                    with open(file_descriptor_process_profiler_file, "a", encoding="utf-8") as f:
                        f.write(f"{{time.ctime()}} - File Descriptor Alert - Above Threshold {file_descriptor_threshold} - Process: [ {process_name} ], PID: {{int(find_pid_by_name('{process_name}'))}}, File Descriptors: {{find_file_descriptor_usage_by_pid(int(find_pid_by_name('{process_name}')))}}\\n")
                        process_action = subprocess.run(['{action}'], capture_output=True, text=True)
                        time.sleep(5)
                        f.write(f"{{time.ctime()}} - File Descriptor Alert - After Remediation - Action Taken: [ {action} ], Process: [ {process_name} ], PID: {{int(find_pid_by_name('{process_name}'))}}, File Descriptors: {{find_file_descriptor_usage_by_pid(int(find_pid_by_name('{process_name}')))}}\\n")
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
    write_to_file(os.path.abspath(f"../watch_list/{sanitized_filename}_fds.py"), textwrap.dedent(template))