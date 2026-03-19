import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from datetime import datetime

ROOT = Path("C:/AI/Tutor")
LOG_DIR = ROOT / "logs" / "filesystem"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / f"fs_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.log"


class FileWatcher(FileSystemEventHandler):

    def log(self, event_type, path):
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.utcnow()} | {event_type} | {path}\n")

    def on_created(self, event):
        self.log("CREATED", event.src_path)

    def on_modified(self, event):
        self.log("MODIFIED", event.src_path)

    def on_deleted(self, event):
        self.log("DELETED", event.src_path)


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(FileWatcher(), str(ROOT), recursive=True)
    observer.start()

    print("Tutor filesystem watcher running...")

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()