#  Echo Chat

A Streamlit chatbot powered by Google Gemini. Upload a PDF and ask questions about it — the app uses TF-IDF retrieval (RAG) to find relevant excerpts and feeds them to the model.

**Live demo:** https://echobotgit-rishi.streamlit.app/

---

## Features

- Four built-in AI personalities (Trainer, Poet, Geek, German)
- Custom personality via free-text instruction
- PDF upload with TF-IDF-based retrieval (RAG)
- Powered by `gemini-2.5-flash`

---

## Prerequisites

- A **Gemini API key** — get one free at https://aistudio.google.com/app/apikey

---

## Running Locally (without Docker)


### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API key

Create a `.env` file in the project root:

```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

Or copy the example and fill it in:

```bash
cp .env.example .env
# then edit .env with your key
```

### 4. Run the app

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## Running with Docker

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### 1. Set your API key

Create a `.env` file in the project root (Docker Compose reads it automatically):

```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 2. Build and start

```bash
docker compose up --build
```

Open **http://localhost:8501** in your browser.

The `--build` flag is only needed the first time, or after you change `requirements.txt`. For subsequent starts:

```bash
docker compose up
```

### 3. Stop the app

```bash
# Stop but keep the container (fast restart later)
docker compose stop

# Stop and remove the container entirely
docker compose down
```

### 4. Updating code

Since the source folder is mounted into the container, you can edit `app.py` freely. Streamlit's file watcher is disabled inside Docker for stability, so to pick up changes just restart:

```bash
docker compose restart app
```

Or stop and start again:

```bash
docker compose down && docker compose up
```

---


## Environment Variables

`GEMINI_API_KEY` 

---

## Notes

- The app also supports Streamlit's built-in secrets manager (`st.secrets`). If you're deploying to Streamlit Community Cloud, add your key there instead of using a `.env` file.
- PDF content is processed in-memory and is not persisted between sessions.
