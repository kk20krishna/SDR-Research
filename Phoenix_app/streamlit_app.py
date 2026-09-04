import os
import stat
import subprocess
import sys
import gdown

GDRIVE_FILE_ID = "14JPtuzttivq8JEcfcEBN9Pam3FVTHKJk"
LOCAL_DB_PATH = "phoenix.db"

# 1. Download SQLite DB from Google Drive if not present
if not os.path.exists(LOCAL_DB_PATH):
    print("Downloading SQLite DB from Google Drive...")
    url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
    gdown.download(url, LOCAL_DB_PATH, quiet=False)

    # Read-only permissions
    os.chmod(LOCAL_DB_PATH, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

# 2. Set Phoenix Environment Variables
abs_path = os.path.abspath(LOCAL_DB_PATH)
port = os.environ.get("PORT", "10000")

env = os.environ.copy()
env["PHOENIX_HOST"] = "0.0.0.0"
env["PHOENIX_PORT"] = str(port)
env["PHOENIX_SQL_DATABASE_URL"] = f"sqlite:///file:{abs_path}?mode=ro&uri=true"

print(f"Launching Phoenix on port {port}...")

# 3. Exec Phoenix directly using its official CLI command
sys.exit(
    subprocess.call(
        [sys.executable, "-m", "phoenix.server.main", "serve"],
        env=env
    )
)
