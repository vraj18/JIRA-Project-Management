#!/usr/bin/env python3
"""
free_pizza.py

Usage:
  - Run with built-in sample data:
      python3 free_pizza.py
  - Run with a CSV input (columns: customer,order_price):
      python3 free_pizza.py --csv sample_data.csv --min-orders 2 --min-price 100
  - Run with custom min params:
      python3 free_pizza.py --min-orders 3 --min-price 150

Outputs (saved to current directory):
  - total_sales.png       (bar chart of total sales per customer)
  - income_share.png      (pie chart of income share by customer)
  - summary.csv           (CSV summary: customer,total_orders,qualifying_orders,total_sales,avg_order)
  - prints eligible customers to stdout
"""

import argparse
import csv
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

import pandas as pd
import matplotlib.pyplot as plt


def eligible_customers(customers_dict: Dict[str, List[float]], min_orders: int, min_price: float) -> Tuple[List[str], pd.DataFrame]:
    """
    Determine eligible customers and return a summary dataframe.

    customers_dict: dict mapping customer -> list of order prices
    min_orders: minimum number of qualifying orders required for eligibility
    min_price: order price threshold to count as qualifying

    Returns:
      (eligible_list, df_summary)
    """
    rows = []
    eligible = []
    for name, orders in customers_dict.items():
        total_orders = len(orders)
        qualifying_orders = sum(1 for p in orders if p >= min_price)
        total_sales = sum(orders)
        avg_order = total_sales / total_orders if total_orders else 0.0
        rows.append({
            "customer": name,
            "total_orders": total_orders,
            "qualifying_orders": qualifying_orders,
            "total_sales": total_sales,
            "avg_order": round(avg_order, 2)
        })
        if qualifying_orders >= min_orders:
            eligible.append(name)
    df = pd.DataFrame(rows).sort_values(by="total_sales", ascending=False).reset_index(drop=True)
    return eligible, df


def read_csv_to_customers(path: str) -> Dict[str, List[float]]:
    """
    Read CSV with columns: customer,order_price. Returns customers dict.
    Accepts extra columns but only uses the two above.
    """
    customers = defaultdict(list)
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if 'customer' not in reader.fieldnames or 'order_price' not in reader.fieldnames:
            raise ValueError("CSV must contain 'customer' and 'order_price' columns")
        for r in reader:
            name = r['customer'].strip()
            try:
                price = float(r['order_price'])
            except Exception:
                # skip invalid rows but warn
                print(f"Warning: skipping row with invalid order_price: {r}", file=sys.stderr)
                continue
            customers[name].append(price)
    return customers


def plot_and_save(df: pd.DataFrame, out_bar: str = "total_sales.png", out_pie: str = "income_share.png") -> None:
    # Bar chart: total sales per customer
    plt.figure(figsize=(8, 4))
    plt.bar(df['customer'], df['total_sales'])
    plt.title('Total sales per customer')
    plt.xlabel('Customer')
    plt.ylabel('Total sales (Rs)')
    plt.tight_layout()
    plt.savefig(out_bar)
    plt.close()

    # Pie chart: income share by customer
    plt.figure(figsize=(6, 6))
    plt.pie(df['total_sales'], labels=df['customer'], autopct='%1.1f%%')
    plt.title('Income share by customer')
    plt.tight_layout()
    plt.savefig(out_pie)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Find customers eligible for a free pizza and visualize sales.")
    parser.add_argument("--csv", type=str, help="Path to CSV with columns: customer,order_price")
    parser.add_argument("--min-orders", type=int, default=2, help="Minimum qualifying orders required (default 2)")
    parser.add_argument("--min-price", type=float, default=100.0, help="Minimum price to count as qualifying (default 100.0)")
    parser.add_argument("--out-summary", type=str, default="summary.csv", help="Output summary CSV file path")
    parser.add_argument("--out-bar", type=str, default="total_sales.png", help="Output bar chart path")
    parser.add_argument("--out-pie", type=str, default="income_share.png", help="Output pie chart path")

    args = parser.parse_args()

    # Sample data used if no CSV provided
    sample_customers = {
        "Alice": [120, 80, 150],
        "Bob": [200, 50],
        "Charlie": [30, 40, 20],
        "Diana": [300, 350, 400, 100],
        "Eve": [80, 120, 130],
        "Frank": [500],
    }

    #edit 1
    #edit 2

    if args.csv:
        try:
            customers = read_csv_to_customers(args.csv)
        except Exception as e:
            print(f"Error reading CSV: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        customers = sample_customers

    eligible, df = eligible_customers(customers, args.min_orders, args.min_price)

    # Save summary CSV
    df.to_csv(args.out_summary, index=False)
    print(f"Saved summary to {args.out_summary}")

    # Save plots
    plot_and_save(df, args.out_bar, args.out_pie)
    print(f"Saved bar chart to {args.out_bar} and pie chart to {args.out_pie}")

    # Print eligible customers
    print(f"\nAssumption: qualifying order price >= {args.min_price}, min qualifying orders = {args.min_orders}")
    print("Eligible customers for a free pizza:", eligible)


if __name__ == "__main__":
    main()
