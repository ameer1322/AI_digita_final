# AI Digital Store

An Amazon-like e-commerce store with an AI-powered chat assistant that helps users find and learn about products.

## Features

- Browse and purchase products
- Order management and order history
- Favorites list
- AI chat assistant to answer questions about available products
- User authentication

## Tech Stack

- **Backend:** FastAPI, MySQL, Redis
- **Frontend:** Streamlit
- **AI:** OpenAI GPT
- **Infrastructure:** Docker

## Installation & Setup

### Prerequisites

- Python 3.11+
- Docker

### 1. Clone the repository

```bash
git clone https://github.com/ameer1322/AI_digita_final.git
cd AI_digita_final
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the database and Redis

```bash
docker compose up
```

### 4. Set your API key

In `config/config.py`, set your OpenAI API key:

```python
os.environ["OPENAI_API_KEY"] = "your_key_here"
```

### 5. Run the backend

```bash
uvicorn main:app --reload
```

### 6. Run the frontend

```bash
streamlit run .\ui\multipage_app\landing.py
```