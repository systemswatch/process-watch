#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import os
from general_process_profiler import general_process_profiler
from memory_process_profiler import memory_process_profiler
from file_descriptor_process_profiler import file_descriptor_process_profiler

# Menu ANSI Colors
BLACK = '\033[30m'
GREEN = '\033[32m'
BOLD_GREEN = '\033[1;32m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_RED = '\033[91m'
BOLD_CYAN = '\033[1;36m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_BOLD_BLUE = '\033[1;94m'
BACKGROUND_BRIGHT_MAGENTA = '\033[105m'
RESET = '\033[0m'

# Reset Sceen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Create the watch_list directory to store configurations
def create_watch_list_directory_if_not_exists(watch_list_path):
    if not os.path.exists(watch_list_path):
        os.makedirs(watch_list_path)
        print(f"{GREEN}Directory '{watch_list_path}' created.{RESET}")

# List configurations in the watch_list directory
def list_files(directory):
    try:
        files = os.listdir(directory)
        return files
    except FileNotFoundError:
        clear_screen()
        print(f"\n{BLACK}{BACKGROUND_BRIGHT_MAGENTA}Error: Directory '{directory}' not found.{RESET}")
        return []
    except NotADirectoryError:
        clear_screen()
        print(f"\n{BLACK}{BACKGROUND_BRIGHT_MAGENTA}Error: '{directory}' is not a valid directory.{RESET}")
        return []

# Delete a chosen configuration in the watch_list directory
def delete_file(directory, filename):
    watch_list_path = os.path.join(directory, filename)
    try:
        os.remove(watch_list_path)
        clear_screen()
        print(f"\n{BRIGHT_GREEN}'{filename}' configuration deleted successfully.{RESET}")
    except FileNotFoundError:
        clear_screen()
        print(f"\n{BLACK}{BACKGROUND_BRIGHT_MAGENTA}Error: File '{filename}' not found.{RESET}")
    except PermissionError:
        clear_screen()
        print(f"\n{BLACK}{BACKGROUND_BRIGHT_MAGENTA}Error: Permission denied to delete '{filename}'.{RESET}")
    except Exception as e:
        clear_screen()
        print(f"\n{BLACK}{BACKGROUND_BRIGHT_MAGENTA}An error occurred: {e}{RESET}")

# Configuration Tool Menu
def display_menu():
    clear_screen()
    create_watch_list_directory_if_not_exists("../watch_list")
    while True:
        print(f"\n{BRIGHT_GREEN}PROCESS WATCH OPTIONS{RESET}\n")
        print("1. List Configuration Files.")
        print("2. Delete a Configuration.")
        print("3. Create a Process Profiler Configuration.")
        print("4. Quit")
        
        top_choice = input(f"\n{BRIGHT_CYAN}Enter your choice (1-4):{RESET}\n")
        
        if top_choice == '1':
            clear_screen()
            files = list_files("../watch_list")
            if files:
                print(f"\n{BRIGHT_GREEN}CURRENT CONFIGURATION FILES:{RESET}\n")
                for i, file in enumerate(files):
                    print(f"{BRIGHT_YELLOW}{i+1}. {file}{RESET}")
        elif top_choice == '2':
            clear_screen()
            while True:
                files = list_files("../watch_list")
                if files:
                    print(f"\n{BRIGHT_GREEN}CURRENT CONFIGURATION FILES:{RESET}\n")
                    for i, file in enumerate(files):
                        print(f"{BRIGHT_YELLOW}{file}{RESET}")
                filename = input(f"\n{BRIGHT_RED}Enter the{RESET} {BRIGHT_CYAN}name{RESET} {BRIGHT_RED}of the configuration to{RESET} {BRIGHT_RED}delete{RESET}{BRIGHT_YELLOW} ({BRIGHT_CYAN}e to exit{RESET}):{RESET}\n")
                if filename == 'e':
                    clear_screen()
                    break
                delete_file("../watch_list", filename)
        elif top_choice == '3':
            clear_screen()
            while True:
                print(f"\n{BRIGHT_GREEN}PROCESS WATCH CONFIGURATION CREATION OPTIONS{RESET}\n")
                print("1. Create General Process Profiler")
                print("2. Create Memory Process Profiler")
                print("3. Create File Descriptor Profiler")
                print("4. Exit")
                watch_list_choice = input(f"\n{BRIGHT_CYAN}Enter your choice (1-4):{RESET}\n")
                if watch_list_choice == '1':
                    clear_screen()
                    general_process_profiler()
                    break
                if watch_list_choice == '2':
                    clear_screen()
                    memory_process_profiler()
                    break
                if watch_list_choice == '3':
                    clear_screen()
                    file_descriptor_process_profiler()
                    break
                clear_screen()
                if watch_list_choice == '4':
                    break
                clear_screen()
                print(f"\n{BLACK}{BACKGROUND_BRIGHT_MAGENTA}Invalid choice. Please try again.{RESET}")                  
        elif top_choice == '4':
            print(f"\n{BRIGHT_GREEN}Quitting...{RESET}")
            break
        else:
            clear_screen()
            print(f"\n{BLACK}{BACKGROUND_BRIGHT_MAGENTA}Invalid choice. Please try again.{RESET}")

if __name__ == "__main__":
    display_menu()
