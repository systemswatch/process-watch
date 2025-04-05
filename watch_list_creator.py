import os
import textwrap
def write_to_file(filename, template):
    try:
        with open(filename, 'w') as file:
            file.write(template)
        print(f"Text successfully written to '{filename}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def display_menu():
    while True:
        print("\nOptions:")
        print("1. Make Logging Watch List Configuration")
        print("2. Exit")
        
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == '1':
            filename = input("Enter the logging watch list configuration file to create: ")
            service_name = input("Enter the service name to monitor: ")
            interval = input("Enter the monitoring interval in seconds: ")
            template = f"""
            import os
            import sys
            import time
            import logging
            import threading
            import psutil

            output_file = (f"{{str(os.getcwd())}}/process_watch.out")

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
            write_to_file(f"{str(os.getcwd())}/watch_list/{filename}.py", textwrap.dedent(template))
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    display_menu()
