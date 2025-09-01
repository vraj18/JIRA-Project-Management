import pytest
from free_pizza import eligible_customers

def test_no_customers():
    customers = {}
    eligible, df = eligible_customers(customers, 1, 100)
    assert eligible == []
    assert df.empty

def test_simple_eligibility():
    customers = {"A": [100, 120], "B": [50, 60]}
    eligible, df = eligible_customers(customers, 2, 100)
    assert eligible == ["A"]
    assert "A" in df['customer'].values

def test_edge_min_price():
    customers = {"A": [99.99, 100.0, 100.0], "B": [100.0]}
    eligible, df = eligible_customers(customers, 2, 100.0)
    assert "A" in eligible
    assert "B" not in eligible

def test_avg_calculation_and_order_counts():
    customers = {"X": [10,20,30], "Y": [100]}
    eligible, df = eligible_customers(customers, 1, 50)
    # Y should be eligible (one order >=50)
    assert "Y" in eligible
    # Check dataframe columns present
    assert set(["customer","total_orders","qualifying_orders","total_sales","avg_order"]).issubset(set(df.columns))
