import os
import json
import subprocess
import time
from datetime import datetime
from multiprocessing import Pool, Manager
import tkinter as tk
import threading
from extraction_utils import extract_valuable_info  
from logging import write_log

start_stamp = datetime.now().strftime('%m%d_%H%M_%S')

NDJSON_FILE = rf".\data\json\data_{start_stamp}.ndjson"
LOG_FILE = rf".\logs\log_{start_stamp}.log"

lock = None
scraper_count = 1

def scrape_tag(params):
    tag, lock, status_dict = params
    temp_file = rf".\data\temp\temp_{tag}.json"
    status_dict[tag] = "running"

    # Run the Node.js scraper script
    result = subprocess.Popen(
        ['node', r'.\src\scraper.js', tag],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8',
        errors='replace',
        text=True
    )
    nopid = result.pid # PID of the Node.js subprocess
    pipid = os.getpid() # PID of the Python process

    #write_log(lock, pipid, nopid, f"[INFORMATION] Started scraping for #{tag}")
    print(f"⚙️  Scraping \033[1;92m#{tag}\033[0m", end="\r")

    stdout, stderr = result.communicate()

    # Handle errors from the scraper
    if stderr:
        print(f"❗ Scraper error for #{tag}:\n{stderr.strip()}")
        #write_log(lock, pipid, nopid, f"[ERROR] Error scraping #{tag}: {stderr.strip()}")
        status_dict["session"]["Errors"] += 1

    # try to load and process the scraped data
    try:
        if not os.path.exists(temp_file): # prevent open cotext manager from raising an error
            raise FileNotFoundError(f"Temporary file {temp_file} not found.")

        with open(temp_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        extracted = [extract_valuable_info(entry, tag) for entry in data]

    except json.JSONDecodeError:
        #write_log(lock, pipid, nopid, f"[WARNING] No valid data for #{tag}")
        print(f"⚠️  No valid data for tag: \033[1;91m#{tag}\033[0m")
        status_dict["session"]["Invalid"] += 1
        status_dict[tag] = "invalid"
        return 0

    # Write extracted data to the NDJSON file
    with lock:
        with open(NDJSON_FILE, "a", encoding="utf-8") as f:
            for item in extracted:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    #write_log(lock, pipid, nopid, f"[INFORMATION] Scraped {len(extracted)} videos under #{tag}")
    print(f"✅ Scraped \033[1;92m{len(extracted)}\033[0m videos under \033[1;92m#{tag}\033[0m")

    # Update session statistics
    if len(extracted) == 0:
        status_dict["session"]["Misses"] += 1
        write_log(lock, pipid, nopid, f"[WARNING] Missed videos for #{tag}")
        print(f"⚠️ Missed videos for \033[1;91m#{tag}\033[0m")
        status_dict[tag] = "missed"
    else:
        status_dict["session"]["Videos Scraped"] += len(extracted)
        status_dict["session"]["Tags Scraped"] += 1
        status_dict[tag] = "finished"

    # Clean up and update status
    os.remove(temp_file)
    status_dict["session"]["Prev Videos"] = len(extracted)
    status_dict["session"]["Prev Tag"] = tag
    
    #write_log(lock, pipid, nopid, f"[INFORMATION] Finished scraping for #{tag}")
    print(f"✅ Finished scraping for \033[1;92m#{tag}\033[0m")
    return 0

def process_pool(tags, lock, status_dict):
    jobs = [(tag, lock, status_dict) for tag in tags]
    with Pool(scraper_count) as pool:
        pool.map(scrape_tag, jobs)

def get_tags():
    print("🔍 Checking scraped tags in json file...")
    scraped_tags = set()
    if os.path.exists(NDJSON_FILE):
        with open(NDJSON_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    scraped_tags.add(entry["tag"])
                except Exception:
                    continue

    with open("data\\tags.txt", "r", encoding="utf-8") as f:
        tags = [
            line.strip()
            for line in f
            if line.strip() not in scraped_tags
        ]
    return tags

def update_gui(tags, status_dict, labels, time_running):
    time_running += 0.25
    s = status_dict["session"]

    # Update average stat
    if s["Tags Scraped"] > 0: s["Average"] = s["Videos Scraped"] // s["Tags Scraped"]
    

    # Update status_labels with status_dict values
    pending = len([v for v in status_dict.values() if v == "pending"])
    running = ', '.join([k for (k, v) in status_dict.items() if v == "running"])
    finished = len([v for v in status_dict.values() if v not in ("pending", "running")])-1 # Exclude "session" key from finished count

    labels[0][0].config(text=f"Pending: {pending}")
    labels[0][1].config(text=f"Running: {running}")
    labels[0][2].config(text=f"Finished: {finished}")

    # Update session_labels with current status_dict["session"] values
    for i, (k, v) in enumerate(s.items()):
        if i < len(labels[1]):
            
            labels[1][i].config(text=f"{k}: {v}")

    # Update time running label
    labels[2].config(text=f"Time Running: {time.strftime('%H:%M:%S', time.gmtime(time_running))}")

    # Update the GUI every 250ms
    root.after(250, update_gui, tags, status_dict, labels, time_running)

from datetime import datetime

if __name__ == "__main__":
    manager = Manager()
    lock = manager.Lock()
    status_dict = manager.dict()
    status_dict["session"] = manager.dict({
        "Videos Scraped": 0,
        "Tags Scraped": 0,
        "Prev Videos": 0,
        "Prev Tag": 0,
        "Average": 0,
        "Misses": 0,
        "Invalid": 0,
        "Errors": 0
    })

    root = tk.Tk()
    root.title("TikTok Scraper")
    root.geometry("300x700")
    font = ("Arial", 16)
    time_running = 0.0
    

    tags = get_tags()
    for tag in tags:
        status_dict[tag] = "pending"

    status_grid = tk.Frame(root, relief="ridge", bd=5)
    session_grid = tk.Frame(root, relief="ridge", bd=5)

    time_running_label = tk.Label(root, text="Time Running: 00:00:00", font=font, relief="ridge", bd=5)
    status_labels = [
    tk.Label(status_grid, text=f"Pending: {len([v for v in status_dict.values() if v == 'pending'])}", font=font),
    tk.Label(status_grid, text=f"Running: {', '.join([k for k, v in status_dict.items() if v == 'running'])}", font=font),
    tk.Label(status_grid, text=f"Finished: {len([v for v in status_dict.values() if v == 'finished'])}", font=font),
    ]
    
    try:
        session_labels = [tk.Label(session_grid, text=f"{k}: {v}", font=font) for k, v in status_dict["session"].items()]
    except Exception as e:
        print(f"Error encountered while creating labels: {e}")

    for i, label in enumerate(status_labels):
        label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

    for i, label in enumerate(session_labels):
        label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

    labels = [status_labels, session_labels, time_running_label]
    frames = [time_running_label, status_grid, session_grid]
    
    for n, i in enumerate(frames):
        i.grid(row=n, column=0, padx=10, pady=10, sticky="ew")
        
    

    scraper_thread = threading.Thread(target=process_pool, args=(tags, lock, status_dict), daemon=True)
    scraper_thread.start()

    root.after(250, update_gui, tags, status_dict, labels, time_running)
    root.mainloop()


