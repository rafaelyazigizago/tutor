import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path("C:/AI/Tutor")
LOG_DIR = ROOT / "logs" / "git"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / f"git_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.log"


def log_commits():

    result = subprocess.run(
        ["git", "log", "--pretty=format:%H | %an | %ad | %s"],
        capture_output=True,
        text=True
    )

    with open(LOG_FILE, "w") as f:
        f.write(result.stdout)


if __name__ == "__main__":
    log_commits()