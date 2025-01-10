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

# Configure Logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
)

# Write PID File
def write_pid_file():
    try:
        with open(pid_file, 'w', encoding="utf-8") as f:
            f.write(str(os.getpid()))
            setproctitle(f"Process Watch - PID {str(os.getpid())}")
    except Exception as e: 
        logging.error("An error occurred writing the daemon pid file:", exc_info=True)
        raise sys.exit(1)

# Read PID File
#def read_pid_file():
#    try:
#        with open(pid_file, 'r', encoding="utf-8") as f:
#            pid_number = int(f.read().strip())
#    except Exception as e:
#        logging.error("An error occurred reading the daemon pid file:", exc_info=True)
#        raise sys.exit(1)

# Daemonize
def processwatch():

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

    write_pid_file()

    # Run Daemon Logic
    while True:
        try:
            a = 1 / 0
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"Daemon running at {time.ctime()}\n")
            time.sleep(10)
        except Exception as e:
            logging.error("An error occurred in the daemon:", exc_info=True)
            raise sys.exit(1)

if __name__ == "__main__":
    processwatch()
