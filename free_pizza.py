import matplotlib.pyplot as plt
import pandas as pd

def free_pizza(customers: dict, min_orders: int, min_price: float):
    
    rows = []
    eligible = []

    # Process each customer
    for name, orders in customers.items():
        total_orders = len(orders)
        qualifying_orders = sum(1 for p in orders if p >= min_price)
        total_sales = sum(orders)
        avg_order = round(total_sales / total_orders, 2) if total_orders else 0.0

        rows.append({
            "customer": name,
            "total_orders": total_orders,
            "qualifying_orders": qualifying_orders,
            "total_sales": total_sales,
            "avg_order": avg_order,
        })

        if qualifying_orders >= min_orders:
            eligible.append(name)

    # Create DataFrame for easier visualization
    df = pd.DataFrame(rows).sort_values(by="total_sales", ascending=False)

    # --- Visualization 1: Bar chart (Total sales per customer) ---
    plt.bar(df["customer"], df["total_sales"])
    plt.title("Total Sales per Customer")
    plt.xlabel("Customer")
    plt.ylabel("Total Sales (Rs)")
    plt.tight_layout()
    plt.show()

    # --- Visualization 2: Pie chart (Income share) ---
    plt.pie(df["total_sales"], labels=df["customer"], autopct="%1.1f%%")
    plt.title("Income Share by Customer")
    plt.tight_layout()
    plt.show()

    return eligible


# --- Example usage ---
if __name__ == "__main__":
    customers_data = {
        "Alice": [120, 80, 150],
        "Bob": [200, 50],
        "Charlie": [30, 40, 20],
        "Diana": [300, 350, 400, 100],
        "Eve": [80, 120, 130],
        "Frank": [500],
    }

    result = free_pizza(customers_data, min_orders=2, min_price=100)
    print("Eligible customers for a free pizza:", result)
