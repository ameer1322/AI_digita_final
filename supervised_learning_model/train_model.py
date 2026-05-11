import pandas as pd
import numpy as np
import mysql.connector
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

from config.config import config


conn = mysql.connector.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    database=config.MYSQL_DATABASE,
    port=int(config.MYSQL_PORT)
)

# ─────────────────────────────────────────────
# 2. PULL & BUILD FEATURES FROM REAL DATA
# ─────────────────────────────────────────────
query = """
SELECT
    users_1.user_id,
    COUNT(DISTINCT orders_1) AS total_orders,
    SUM (order_product_1 * product_1.price) AS total_spent,
    AVG(order_totals.order_total) AS avg_order_spend,
    SUM(order_product_1.quantity) AS total_items_bought,
    last_order.last_order_total AS next_order_spend

FROM users users_1

JOIN orders orders_1
    ON users_1.user_id = orders_1.user_id AND orders_1.order_status = "CLOSED"

JOIN order_product order_product_1
    ON orders_1.order_id = order_product_1.order_id

JOIN products products_1
    ON order_product_1.product_id = products.product_id


JOIN (
    SELECT order_product_2.order_id, SUM(order_product_2.quantity * products_2.price) AS order_total
    FROM order_product order_product_2
    JOIN products products_2 ON order_product_2.products_id = products_2.product_id
    GROUP BY op2.order_id 
) AS order_totals ON orders_1.order_id = order_totals.order_id

JOIN (
    SELECT orders_3.user_id, SUM(order_product_3.quantity * products_3.price) AS last_order_total
    FROM orders orders_3
    JOIN order_product order_product_3 ON orders_3.order_id = order_product_3.order_id
    JOIN product products_3 ON order_product_3.product_id = product_3.product_id
    WHERE orders_3.order_id = (
        SELECT order_id from orders
        WHERE user_id = orders_3.user_id AND order_status = "CLOSED"
        ORDER BY order_date DESC
        LIMIT 1
    )
    GROUP BY orders_3.user_id
)AS last_order ON u.user_id = last_order.user_id

GROUP BY users_1.user_id
HAVING total_orders > 5
"""

df = pd.read_sql(query, conn)
conn.close()

print(f"✅ Loaded {len(df)} users from database")
print(df.head(10).to_string())

# Save dataset for submission
df.to_csv("user_dataset.csv", index=False)
print("\n✅ Dataset saved to user_dataset.csv")

# ─────────────────────────────────────────────
# 3. TRAIN THE MODEL
# ─────────────────────────────────────────────
FEATURES = [
    "total_orders",
    "total_spent",
    "avg_order_spend",
    "total_items_bought"
]
TARGET = "next_order_spend"

# Drop rows with nulls
df = df.dropna(subset=FEATURES + [TARGET])

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ─────────────────────────────────────────────
# 4. EVALUATE
# ─────────────────────────────────────────────
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2  = r2_score(y_test, y_pred)

print(f"\n📊 Model Evaluation")
print(f"   MAE : ${mae:.2f}  (average prediction error in dollars)")
print(f"   R²  : {r2:.3f}   (1.0 = perfect, >0.7 is good)")

importances = pd.Series(model.feature_importances_, index=FEATURES)
print("\n🔍 Feature Importances (what drives spend the most):")
print(importances.sort_values(ascending=False).to_string())

# ─────────────────────────────────────────────
# 5. SAVE MODEL
# ─────────────────────────────────────────────
joblib.dump(model, "spend_model.pkl")
print("\n✅ Model saved to spend_model.pkl")
