#!/usr/bin/env python3

import os
import textwrap

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

# Global System Processes Profiler Menu
def global_system_processes_profiler():
    print(f"\n{BRIGHT_GREEN}GLOBAL SYSTEM PROCESSES PROFILER SETTINGS:{RESET}")
    filename = "system-processes"
    while True:
        try:
            interval = int(input(f"\n{BRIGHT_CYAN}Enter the monitoring interval {GREEN}(in seconds, recommend 1800 (30min)){RESET}:{RESET}\n"))
            break
        except ValueError:
            print(f"{BLACK}{BACKGROUND_BRIGHT_MAGENTA}\nInvalid input. Please enter a number of seconds.{RESET}")

    template = f"""
    # Global System Processes Profiler
    import os
    import sys
    import time
    import logging
    import threading
    import psutil
    import operator
    import subprocess

    global_system_processes_profiler_file = (f"{{str(os.getcwd())}}/logs/glbl-sys-procs-profiler.log")
    error_file = (f"{{str(os.getcwd())}}/logs/error.log")

    # Global File Descriptor Counter

    def get_top_processes(num_top=5):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'num_threads', 'num_fds', 'memory_info', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        top_threads = sorted(processes, key=lambda p: p['num_threads'], reverse=True)[:num_top]
        top_fds = sorted(processes, key=lambda p: p['num_fds'], reverse=True)[:num_top]
        top_memory = sorted(processes, key=lambda p: p['memory_info'].rss, reverse=True)[:num_top]
        top_cpu = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:num_top]

        return top_threads, top_fds, top_memory, top_cpu

    def monitor():
        while True:
            try:
                top_threads, top_fds, top_memory, top_cpu = get_top_processes()
                with open(global_system_processes_profiler_file, "a", encoding="utf-8") as f:
                    f.write(f"########### Top 5 Memory (RSS) Consumers - {{time.ctime()}} ###########\\n")
                    for proc in top_memory:
                        f.write(f"{{time.ctime()}} - Top Memory (RSS) Consumer - Name: {{proc['name']}}, PID: {{proc['pid']}}, Memory (RSS): {{proc['memory_info'].rss}} bytes\\n")
                    f.write(f"########### Top 5 CPU Consumers - {{time.ctime()}} ###########\\n")
                    for proc in top_cpu:
                        f.write(f"{{time.ctime()}} - Top CPU Consumer - Name: {{proc['name']}}, PID: {{proc['pid']}}, CPU: {{proc['cpu_percent']}}%\\n")
                    f.write(f"########### Top 5 Thread Consumers - {{time.ctime()}} ###########\\n")
                    for proc in top_threads:
                        f.write(f"{{time.ctime()}} - Top Thread Consumer - Name: {{proc['name']}}, PID: {{proc['pid']}}, Threads: {{proc['num_threads']}}\\n")
                    f.write(f"########### Top 5 File Descriptor Consumers - {{time.ctime()}} ###########\\n")
                    for proc in top_fds:
                        f.write(f"{{time.ctime()}} - Top File Descriptor Consumer - Name: {{proc['name']}}, PID: {{proc['pid']}}, File Descriptors: {{proc['num_fds']}}\\n")
                time.sleep({interval})
            except Exception as e:
                print(f"An error occurred in Process Watch configuration file {filename}: {{e}}")
                with open(error_file, "a", encoding="utf-8") as file:
                    file.write(str(e) + (f" in {filename}") + "\\n")
                    raise sys.exit(1)

    def worker():
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.start()

    worker()
    """
    # Write the template into a config
    write_to_file(os.path.abspath(f"../watch_list/{filename}_glbl.py"), textwrap.dedent(template))