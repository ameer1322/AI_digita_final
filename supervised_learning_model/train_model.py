import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from joblib import dump
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
from config.config import config
import pymysql

conn = pymysql.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    database=config.MYSQL_DATABASE,
    port=int(config.MYSQL_PORT)
)



query = """
SELECT
    users_1.user_id,
    COUNT(DISTINCT orders_1.order_id) AS total_orders,
    SUM(order_product_1.quantity * products_1.price) AS total_spent,
    AVG(order_totals.order_total) AS avg_order_spend,
    SUM(order_product_1.quantity) AS total_items_bought,
    last_order.last_order_total AS next_order_spend

FROM users users_1

JOIN orders orders_1
    ON users_1.user_id = orders_1.user_id AND orders_1.order_status = "CLOSED"

JOIN order_product order_product_1
    ON orders_1.order_id = order_product_1.order_id

JOIN products products_1
    ON order_product_1.product_id = products_1.product_id


JOIN (
    SELECT order_product_2.order_id, SUM(order_product_2.quantity * products_2.price) AS order_total
    FROM order_product order_product_2
    JOIN products products_2 ON order_product_2.product_id = products_2.product_id
    GROUP BY order_product_2.order_id 
) AS order_totals ON orders_1.order_id = order_totals.order_id

JOIN (
    SELECT orders_3.user_id, SUM(order_product_3.quantity * products_3.price) AS last_order_total
    FROM orders orders_3
    JOIN order_product order_product_3 ON orders_3.order_id = order_product_3.order_id
    JOIN products products_3 ON order_product_3.product_id = products_3.product_id
    WHERE orders_3.order_id = (
        SELECT order_id from orders
        WHERE user_id = orders_3.user_id AND order_status = "CLOSED"
        ORDER BY order_date DESC
        LIMIT 1
    )
    GROUP BY orders_3.user_id
)AS last_order ON users_1.user_id = last_order.user_id

GROUP BY users_1.user_id
HAVING total_orders > 5
"""

df = pd.read_sql(query, conn)

conn.close()

print(f"Total rows loaded: {len(df)}")
print(df)
print(df.dtypes)


print(f"✅ Loaded {len(df)} users from database")
print(df.head(10).to_string())

df.to_csv("user_dataset.csv", index=False)


FEATURES = [
    "total_orders",
    "total_spent",
    "avg_order_spend",
    "total_items_bought"
]
TARGET = "next_order_spend"

df = df.dropna(subset=FEATURES + [TARGET])

X = df[FEATURES]
y = df[TARGET]

#USE TO FIGURE OUT OPTIMAL DEGREE
#
#
# train_rmse_error = []
# test_rmse_error =[]
#
# for degree in range(1,10):
#     poly_converter = PolynomialFeatures(degree=degree, include_bias=False)
#     poly_features = poly_converter.fit_transform(X)
#     X_train, X_test, y_train, y_test = train_test_split(poly_features,y,test_size=0.2,random_state=42)
#     model = LinearRegression()
#     model.fit(X_train,y_train)
#     test_prediction = model.predict(X_test)
#     train_prediction = model.predict(X_train)
#
#     train_rmse = root_mean_squared_error(y_train,train_prediction)
#     test_rmse =  root_mean_squared_error(y_test,test_prediction)
#
#     train_rmse_error.append(train_rmse)
#     test_rmse_error.append(test_rmse)
#
# plt.plot(range(1,6), train_rmse_error[:5], label="Train RMSE")
# plt.plot(range(1,6), test_rmse_error[:5], label="Test RMSE")
#
# plt.xlabel("Degree of poly")
# plt.ylabel("RMSE")
# plt.legend()
# plt.show()


#Use when optimal degree is known.
#Optimal degree is 4

optimal_degree = 4
final_poly_converter = PolynomialFeatures(degree=optimal_degree, include_bias=False)
final_model = LinearRegression()

fully_converted_x = final_poly_converter.fit_transform(X)
final_model.fit(fully_converted_x,y)

dump(final_model, "spend_model.pkl")
print("Model saved to spend_model.pkl")
