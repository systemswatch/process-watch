#!/usr/bin/env python
import os
import textwrap

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

# Write configuration file to watch_list directory
def write_to_file(filename, template):
    try:
        with open(os.path.join(os.pardir, "watch_list", filename), 'w', encoding="utf-8") as file:
            file.write(template)
        clear_screen()
        print(f"\n{GREEN}'{filename}' configuration created.{RESET}")
    except Exception as e:
        print(f"{BLACK}{BACKGROUND_BRIGHT_MAGENTA}\nAn error occurred: {e}{RESET}")

# Service Profiler Menu
def service_profiler():
    print(f"\n{BRIGHT_GREEN}SERVICE PROFILER SETTINGS:{RESET}")
    filename = input(f"\n{BRIGHT_CYAN}Enter the name of the configuration file:{RESET}\n")
    sanitized_filename = filename.replace(".", "-")
    service_name = input(f"\n{BRIGHT_CYAN}Enter the service name to monitor:{RESET}\n")
    interval = input(f"\n{BRIGHT_CYAN}Enter the monitoring interval in seconds:{RESET}\n")
    # Service Profiler Template
    template = f"""
    import os
    import sys
    import time
    import logging
    import threading
    import psutil

    output_file = (f"{{str(os.getcwd())}}/logs/process_watch.log")

    # Identify Process By Name Return PID
    def find_procs_by_name(name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == name:
                pid =  proc.info['pid']
        if pid:
            return pid
        else:
            return ("Process N/A.")

    # Identify Process By Name Return Memory Usage
    def find_memory_by_name(name):
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            if proc.info['name'] == name:
                memory_usage = proc.info['memory_info'].rss
        if memory_usage:
            return (f"{{memory_usage / (1024 * 1024):.2f}}")
        else:
            return ("Process N/A.")

    # Identify Process By Name Return CPU % Usage
    def find_cpu_by_name(name):
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            if proc.info['name'] == name:
                p = psutil.Process()
                cpu_usage = p.cpu_percent(interval=1)
                cpu_usage = p.cpu_percent(interval=None)
        if cpu_usage:
            return cpu_usage
        else:
            return ("Process not found.")

    def monitor():

        while True:
            try:
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"{service_name} running at {{time.ctime()}} {service_name} PID: {{find_procs_by_name('{service_name}')}}, Memory: {{find_memory_by_name('{service_name}')}}MB, CPU: {{find_cpu_by_name('{service_name}')}}%\\n")
                time.sleep({interval})
            except Exception as e:
                logging.error("An error occurred in Process Watch: %s", e, exc_info=True)
                raise sys.exit(1)

    def worker():
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.start()

    worker()
    """
    # Write the template into the config
    write_to_file(os.path.abspath(f"../watch_list/{sanitized_filename}.py"), textwrap.dedent(template))
