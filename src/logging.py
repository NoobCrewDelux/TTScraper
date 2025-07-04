from time import strftime
LOG_FILE = rf".\logs\log_{strftime('%m%d_%H%M_%S')}.log"

def write_log(lock, pipid, nopid, message):
    with lock:
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            timestamp = strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            log_file.write(f"[{timestamp}] [PID PYTHON:{pipid} NODE:{nopid}] {message}\n")