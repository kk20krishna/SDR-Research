import os
import stat
import gdown
import phoenix as px
import streamlit as st
import streamlit.components.v1 as components

# --- Configuration ---
# Replace with your actual Google Drive File ID
GDRIVE_FILE_ID = "Y11FRH8o33D31ggeatROOKk3GxMqJ6rOca"
LOCAL_DB_PATH = "phoenix.db"

st.set_page_config(page_title="Arize Phoenix Viewer", layout="wide")


@st.cache_resource(show_spinner="Downloading SQLite DB from Google Drive...")
def download_sqlite_from_gdrive(file_id: str, local_path: str) -> str:
    """Download public file via gdown and set OS-level read-only permissions."""
    if not os.path.exists(local_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        output = gdown.download(url, local_path, quiet=False)

        if output is None or not os.path.exists(local_path):
            raise RuntimeError(
                "Download failed. Check that the file ID is correct and "
                "link sharing is set to 'Anyone with the link can view'."
            )

        # Enforce OS-level read-only access (r--r--r--)
        os.chmod(local_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

    return os.path.abspath(local_path)


@st.cache_resource
def start_phoenix_server(db_path: str):
    """Start Phoenix server connected to SQLite in read-only mode."""
    # SQLite URI with read-only flag
    os.environ["PHOENIX_SQL_DATABASE_URL"] = f"sqlite:///file:{db_path}?mode=ro&uri=true"

    session = px.launch_app(host="127.0.0.1", port=6006)
    return session.url


# --- Main App ---
try:
    local_db = download_sqlite_from_gdrive(GDRIVE_FILE_ID, LOCAL_DB_PATH)
    phoenix_url = start_phoenix_server(local_db)

    # Embed Phoenix UI in Streamlit
    components.iframe(phoenix_url, height=900, scrolling=True)

except Exception as e:
    st.error(f"Failed to load Phoenix: {e}")
