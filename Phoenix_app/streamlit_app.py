import os
import subprocess
import sys
import gdown

GDRIVE_FILE_ID = "14JPtuzttivq8JEcfcEBN9Pam3FVTHKJk"
LOCAL_DB_PATH = "phoenix.db"

# 1. Download SQLite DB from Google Drive if not present
if not os.path.exists(LOCAL_DB_PATH):
    print("Downloading SQLite DB from Google Drive...", flush=True)
    url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
    gdown.download(url, LOCAL_DB_PATH, quiet=False)

# 2. Configure Phoenix Environment
abs_path = os.path.abspath(LOCAL_DB_PATH)
port = os.environ.get("PORT", "10000")

env = os.environ.copy()
env["PHOENIX_HOST"] = "0.0.0.0"
env["PHOENIX_PORT"] = str(port)

# Allow read-write locally so Phoenix can perform required startup migrations
# (Render filesystem is ephemeral, so your Google Drive source file cannot be modified)
env["PHOENIX_SQL_DATABASE_URL"] = f"sqlite:///{abs_path}"

print(f"Launching Phoenix on port {port}...", flush=True)

# 3. Start Phoenix server via CLI
sys.exit(
    subprocess.call(
        [sys.executable, "-m", "phoenix.server.main", "serve"],
        env=env
    )
)
