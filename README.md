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

---

# Supervised learning model

## This model predicts the amount the user will spend on his next order based on his order history.

## Directions

### 1.Start the database

```commandline
docker compose up
```

### 1.Go to the train_model.py file in supervised_learning_model.

### 2.Run the first half of the code in order to find optimal degree for polynomial regression.

### The code will take the users data from the database and create a graph to find the optimal degree. 

### 3.After finding optimal degree for the dataset, run the second half of the code.

### The code will take the users data from the database and train on them, then it will create a supervised learning model and converter as well as a user_dataset for the data it trained on. 

### 4. After training the model, run streamlit:

```commandline
streamlit run .\supervised_learning_model\predictor.py
```

### 5.Enter user id for user you want to make a prediction on