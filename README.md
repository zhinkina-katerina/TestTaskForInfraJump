# City AI Guide

This is a FastAPI-based project that generates interesting places in a selected city using OpenAI (via Pydantic AI), stores requests in a SQLite database, and allows viewing past search history. It includes a Streamlit frontend for interaction.

---

## Features

* FastAPI backend with OpenAI (via Pydantic AI) integration
* SQLite database with Alembic migrations
* Streamlit frontend for user interaction
* Docker + Docker Compose support
* Robust logging and database persistence

---

## Tech Stack

* Python 3.11+
* FastAPI
* Pydantic AI
* SQLAlchemy (Async)
* Alembic
* SQLite
* Streamlit
* Docker + Docker Compose

---

## Development Setup 

### Set up environment variables

Create a `.env` file in the project root with:

```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite+aiosqlite:///./app.db
API_URL=http://localhost:8001
```

## without Docker

### 1. Clone the repository

```bash
git clone https://github.com/your-org/city-ai-guide.git
cd city-ai-guide
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Alembic migrations

```bash
alembic upgrade head
```

### 6. Start the FastAPI server

```bash
python app/main.py
```

### 7. Start the Streamlit frontend

```bash
streamlit run streamlit/app.py
```

---

## Running with Docker

### 1. Build and start the services

```bash
docker-compose up --build
```

### 2. Apply Alembic migrations inside the backend container
```bash
docker-compose exec backend alembic upgrade head
```

## Access the services

* FastAPI API: [http://localhost:8001/docs](http://localhost:8001/docs)
* Streamlit app: [http://localhost:8501](http://localhost:8501)