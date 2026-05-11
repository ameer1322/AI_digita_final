import streamlit as st
import joblib
import numpy as np
import mysql.connector
import os

# ─────────────────────────────────────────────
# DB connection (reuse your existing config)
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",       # your MySQL username
    "password": "",           # your MySQL password
    "database": ""            # your database name
}

# ─────────────────────────────────────────────
# Load model (cached so it only loads once)
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "spend_model.pkl")
    if not os.path.exists(model_path):
        st.error("❌ Model not found. Please run train_model.py first.")
        return None
    return joblib.load(model_path)


# ─────────────────────────────────────────────
# Fetch a real user's features from the DB
# ─────────────────────────────────────────────
def get_user_features(user_id: int) -> dict | None:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            u.age,
            DATEDIFF(NOW(), u.join_date)            AS days_since_joined,
            COUNT(DISTINCT o.order_id)              AS total_orders,
            DATEDIFF(NOW(), MAX(o.order_date))      AS days_since_last_order,
            SUM(op.quantity * p.price)              AS total_spent,
            AVG(order_totals.order_total)           AS avg_order_spend,
            SUM(op.quantity)                        AS total_items_bought,
            COUNT(DISTINCT f.product_id)            AS num_favorites
        FROM users u
        JOIN orders o
            ON u.user_id = o.user_id AND o.order_status = 'CLOSED'
        JOIN order_product op ON o.order_id = op.order_id
        JOIN products p ON op.product_id = p.product_id
        JOIN (
            SELECT op2.order_id, SUM(op2.quantity * p2.price) AS order_total
            FROM order_product op2
            JOIN products p2 ON op2.product_id = p2.product_id
            GROUP BY op2.order_id
        ) AS order_totals ON o.order_id = order_totals.order_id
        LEFT JOIN favorites f ON u.user_id = f.user_id
        WHERE u.user_id = %s
        GROUP BY u.user_id, u.age, u.join_date
    """, (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


# ─────────────────────────────────────────────
# Core prediction function
# ─────────────────────────────────────────────
def predict_spend(features: dict) -> float:
    model = load_model()
    if model is None:
        return 0.0
    X = np.array([[
        features["age"],
        features["days_since_joined"],
        features["total_orders"],
        features["days_since_last_order"],
        features["total_spent"],
        features["avg_order_spend"],
        features["total_items_bought"],
        features["num_favorites"] or 0,
    ]])
    return round(float(model.predict(X)[0]), 2)


# ─────────────────────────────────────────────
# Streamlit page
# ─────────────────────────────────────────────
def show_predictor_page():
    st.title("🛒 User Spend Predictor")
    st.markdown("Predict how much a user is likely to spend on their **next order**, based on their real purchase history.")

    user_id = st.number_input("Enter User ID", min_value=1, step=1, value=1)

    if st.button("🔮 Predict Spend", use_container_width=True):
        with st.spinner("Fetching user data from database..."):
            features = get_user_features(user_id)

        if not features:
            st.error("User not found or has fewer than 2 closed orders — not enough data to predict.")
            return

        prediction = predict_spend(features)

        # Show user stats
        st.subheader("📋 User Stats")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Orders",       int(features["total_orders"]))
        col2.metric("Total Spent",        f"${features['total_spent']:.2f}")
        col3.metric("Avg Order Spend",    f"${features['avg_order_spend']:.2f}")
        col4.metric("Days Since Last Order", int(features["days_since_last_order"]))

        # Prediction result
        st.success(f"💰 Predicted Next Order Spend: **${prediction}**")

        # Business insight
        if prediction > 100:
            st.info("🔥 High-value user — show premium or bundled product recommendations.")
        elif prediction > 40:
            st.info("📦 Medium spender — upsell complementary products or offer free shipping threshold.")
        else:
            st.info("💡 Low spender — try a discount or coupon to increase order value.")


# Run standalone
if __name__ == "__main__":
    show_predictor_page()
