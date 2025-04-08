import sys
sys.dont_write_bytecode = True
import os
import textwrap
from service_profiler import service_profiler

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_watch_list_directory_if_not_exists(watch_list_path):
    if not os.path.exists(watch_list_path):
        os.makedirs(watch_list_path)
        print(f"Directory '{watch_list_path}' created.")

def list_files(directory):
    try:
        files = os.listdir(directory)
        return files
    except FileNotFoundError:
        clear_screen()
        print(f"Error: Directory '{directory}' not found.")
        return []
    except NotADirectoryError:
        clear_screen()
        print(f"Error: '{directory}' is not a valid directory.")
        return []

def delete_file(directory, filename):
    watch_list_path = os.path.join(directory, filename)
    try:
        os.remove(watch_list_path)
        clear_screen()
        print(f"\n'{filename}' watch list configuration deleted successfully.")
    except FileNotFoundError:
        clear_screen()
        print(f"\nError: File '{filename}' not found.")
    except PermissionError:
        clear_screen()
        print(f"\nError: Permission denied to delete '{filename}'.")
    except Exception as e:
        clear_screen()
        print(f"\nAn error occurred: {e}")

def display_menu():
    create_watch_list_directory_if_not_exists("../watch_list")
    while True:
        print("\nProcess Watch Options:\n")
        print("1. List Watch List Configuration Files.")
        print("2. Delete a Watch List Configuration.")
        print("3. Create a Service Profile Watch List Configuration.")
        print("4. Exit")
        
        top_choice = input("\nEnter your choice (1-4):\n")
        
        if top_choice == '1':
            clear_screen()
            files = list_files("../watch_list")
            if files:
                print("\nWatch List Configuration Files:\n")
                for i, file in enumerate(files):
                    print(f"{i+1}. {file}")
        elif top_choice == '2':
            clear_screen()
            filename = input("\nEnter the name of the watch list config to delete:\n")
            delete_file("../watch_list", filename)
        elif top_choice == '3':
            clear_screen()
            while True:
                print("\nProcess Watch Watch List Configuration Choices:\n")
                print("1. Service Profile")
                print("2. Service Profile 2")
                watch_list_choice = input("\nEnter your choice (1-2):\n")
                if watch_list_choice == '1':
                    clear_screen()
                    service_profiler()
                elif watch_list_choice == '2':
                    clear_screen()
                    service_profiler()
                break                  
        elif top_choice == '4':
            print("\nExiting...")
            break
        else:
            clear_screen()
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    display_menu()
