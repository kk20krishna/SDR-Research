import os
import stat
import gdown
import phoenix as px

GDRIVE_FILE_ID = "14JPtuzttivq8JEcfcEBN9Pam3FVTHKJk"
LOCAL_DB_PATH = "phoenix.db"

# 1. Download SQLite database if not present
if not os.path.exists(LOCAL_DB_PATH):
    print("Downloading SQLite DB from Google Drive...")
    url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
    gdown.download(url, LOCAL_DB_PATH, quiet=False)

    # Apply strict OS-level read-only permissions (r--r--r--)
    os.chmod(LOCAL_DB_PATH, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

# 2. Configure Phoenix to use SQLite in read-only mode
abs_path = os.path.abspath(LOCAL_DB_PATH)
os.environ["PHOENIX_SQL_DATABASE_URL"] = f"sqlite:///file:{abs_path}?mode=ro&uri=true"

# 3. Read Render's assigned port (defaults to 10000 on Render)
port = int(os.environ.get("PORT", 10000))

print(f"Starting Phoenix on port {port}...")
px.launch_app(host="0.0.0.0", port=port, run_in_thread=False)
