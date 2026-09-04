import os
import stat
import gdown
import phoenix as px
import streamlit as st
import streamlit.components.v1 as components

# --- Configuration ---
# Replace with your actual Google Drive File ID
GDRIVE_FILE_ID = "14JPtuzttivq8JEcfcEBN9Pam3FVTHKJk"
LOCAL_DB_PATH = "phoenix.db"

st.set_page_config(page_title="Krishna Kumar - SDR Research", layout="wide")

@st.cache_resource(show_spinner="Downloading database...")
def init_db(file_id: str, local_path: str):
    if not os.path.exists(local_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, local_path, quiet=False)
        os.chmod(local_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    
    os.environ["PHOENIX_SQL_DATABASE_URL"] = f"sqlite:///file:{os.path.abspath(local_path)}?mode=ro&uri=true"
    session = px.launch_app()
    return session

try:
    session = init_db(GDRIVE_FILE_ID, LOCAL_DB_PATH)
    
    # Render using Phoenix's native HTML/JS display representation
    ui_html = session._repr_html_()
    st.components.v1.html(ui_html, height=1000, scrolling=True)

except Exception as e:
    st.error(f"Error: {e}")


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
