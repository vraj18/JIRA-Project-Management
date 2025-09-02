import pandas as pd
import matplotlib.pyplot as plt

MIN_ORDERS = 2      
MIN_PRICE = 100.0   

# --- SAMPLE DATA ---
customers = {
    "Alice": [120, 80, 150],
    "Bob": [200, 50],
    "Charlie": [30, 40, 20],
    "Diana": [300, 350, 400, 100],
    "Eve": [80, 120, 130],
    "Frank": [500],
}

rows = []
eligible = []

for name, orders in customers.items():
    total_orders = len(orders)
    qualifying_orders = sum(1 for p in orders if p >= MIN_PRICE)
    total_sales = sum(orders)
    avg_order = round(total_sales / total_orders, 2) if total_orders else 0.0

    rows.append({
        "customer": name,
        "total_orders": total_orders,
        "qualifying_orders": qualifying_orders,
        "total_sales": total_sales,
        "avg_order": avg_order,
    })

    if qualifying_orders >= MIN_ORDERS:
        eligible.append(name)

df = pd.DataFrame(rows).sort_values(by="total_sales", ascending=False)

df.to_csv("summary.csv", index=False)
print("Saved summary.csv")

# --- PLOTS ---
plt.bar(df['customer'], df['total_sales'])
plt.title("Total sales per customer")
plt.xlabel("Customer")
plt.ylabel("Total sales (Rs)")
plt.tight_layout()
plt.savefig("total_sales.png")
plt.close()

plt.pie(df['total_sales'], labels=df['customer'], autopct='%1.1f%%')
plt.title("Income share by customer")
plt.tight_layout()
plt.savefig("income_share.png")
plt.close()

# --- OUTPUT ---
print(f"\nQualifying order price ≥ {MIN_PRICE}, minimum qualifying orders = {MIN_ORDERS}")
print("Eligible customers for a free pizza:", eligible)
