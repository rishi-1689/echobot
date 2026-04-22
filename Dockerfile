# Python 3.12 slim — matches .python-version, much smaller than the full image
FROM python:3.12-slim

WORKDIR /app

# Copy requirements first so Docker can cache this layer.
# If requirements.txt doesn't change, pip install is skipped on rebuilds.
COPY requirements.txt .

# --no-cache-dir keeps the image smaller (no pip download cache needed)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code
COPY . .

EXPOSE 8501

# Streamlit needs these flags to work inside Docker:
# --server.address=0.0.0.0  → listen on all interfaces, not just localhost
# --server.fileWatcherType=none → disables file watcher (inotify issues in containers)
# --browser.gatherUsageStats=false → skip the analytics consent prompt on startup
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.fileWatcherType=none", \
     "--browser.gatherUsageStats=false"]