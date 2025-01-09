import os
import sys
import time
import logging
from setproctitle import setproctitle

#setproctitle("ProcessWatch")
os.makedirs(os.getcwd() + "/pid", exist_ok=True)
os.makedirs(os.getcwd() + "/logs", exist_ok=True)
pid_file = (f"{str(os.getcwd())}/pid/processwatch.pid")
log_file = (f"{str(os.getcwd())}/logs/processwatch.log")
output_file = (f"{str(os.getcwd())}/processwatch.out")

def write_pid_file():
    try:
        with open(pid_file, 'w', encoding="utf-8") as f:
            f.write(str(os.getpid()))
            setproctitle(f"Process Watch - PID {str(os.getpid())}")
    except IOError as e: 
        print(f"An error occurred: {e}")

#def read_pid_file():
#    try:
#        with open(pid_file, 'r', encoding="utf-8") as f:
#            pid_number = int(f.read().strip())
#    except FileNotFoundError as e:
#        print(f"An error occurred: {e}")

def processwatch_log(logf):
    ### This does the "work" of the daemon

    logger = logging.getLogger('processwatch')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logf)
    fh.setLevel(logging.INFO)

    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr)

    fh.setFormatter(formatter)

    logger.addHandler(fh)

def daemonize():
    # Fork the first child process
    pid = os.fork()
    if pid > 0:
        # Exit the parent process
        sys.exit(0)

    # Become a session leader
    os.setsid()

    # Fork the second child process
    pid = os.fork()
    if pid > 0:
        # Exit the first child process
        sys.exit(0)

    # Change the working directory to the root directory
    os.chdir(os.getcwd())

    # Close standard file descriptors
    os.close(0)
    os.close(1)
    os.close(2)

    # Redirect standard file descriptors to /dev/null
    os.open(os.devnull, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)

    processwatch_log(log_file)
    write_pid_file()

    # Run the daemon logic
    while True:
        try:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"Daemon running at {time.ctime()}\n")
            time.sleep(10)
        except IOError as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    daemonize()
