import streamlit as st
import joblib
import numpy as np
import mysql.connector
import sys
import os
import pymysql
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import config

conn = pymysql.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    database=config.MYSQL_DATABASE,
    port=int(config.MYSQL_PORT)
)


@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "spend_model.pkl")
    if not os.path.exists(model_path):
        st.error("Model not found, Please run train_model.py first.")
        return None
    return joblib.load(model_path)

@st.cache_resource
def load_converter():
    converter_path = os.path.join(os.path.dirname(__file__), "spend_model_converter.pkl")
    if not os.path.exists(converter_path):
        st.error("Converter not found, Please run train_model.py first.")
        return None
    return joblib.load(converter_path)



def get_user_features(user_id: int) -> dict | None:
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = """
        SELECT
            users_1.age,
            COUNT(DISTINCT orders_1.order_id) AS total_orders,
            SUM(order_product_1.quantity * products_1.price) AS total_spent,
            AVG(order_totals.order_total) AS avg_order_spend,
            SUM(order_product_1.quantity) AS total_items_bought
        FROM users users_1
        JOIN orders orders_1
            ON users_1.user_id = orders_1.user_id AND orders_1.order_status = 'CLOSED'
        JOIN order_product order_product_1 ON orders_1.order_id = order_product_1.order_id
        JOIN products products_1 ON order_product_1.product_id = products_1.product_id
        JOIN (
            SELECT order_product_2.order_id, SUM(order_product_2.quantity * products_2.price) AS order_total
            FROM order_product order_product_2
            JOIN products products_2 ON order_product_2.product_id = products_2.product_id
            GROUP BY order_product_2.order_id
        ) AS order_totals ON orders_1.order_id = order_totals.order_id
        WHERE users_1.user_id = %s
        GROUP BY users_1.user_id
    """
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row



def predict_spend(features: dict) -> float:
    model = load_model()
    converter = load_converter()
    if model is None:
        return 0.0
    X = np.array([[
        features["total_orders"],
        features["total_spent"],
        features["avg_order_spend"],
        features["total_items_bought"]
    ]])
    X_converted = converter.transform(X)
    return round(float(model.predict(X_converted)[0]), 2)



def show_predictor_page():
    st.title("User Spend Predictor")
    st.write("Predict how much a user is likely to spend on their next order, based on their real purchase history.")

    user_id = st.number_input("Enter User ID", min_value=1, step=1, value=1)

    if st.button("Predict Spend", use_container_width=True):
        with st.spinner("Fetching user data from database..."):
            features = get_user_features(user_id)

        if not features:
            st.error("User not found or has fewer than 2 closed orders — not enough data to predict.")
            return

        prediction = predict_spend(features)

        # Show user stats
        st.subheader("User Stats")
        col1, col2, col3= st.columns(3)
        col1.metric("Total Orders",       int(features["total_orders"]))
        col2.metric("Total Spent",        f"${features['total_spent']}")
        col3.metric("Avg Order Spend",    f"${round(features['avg_order_spend'],2)}")

        st.success(f"Predicted Next Order Spend: ${prediction}")


# Run standalone
if __name__ == "__main__":
    show_predictor_page()
