import pytest

from app.models import Receipt
from app.services.receipt_service import (
    points_for_item_description,
    points_for_item_list_count,
    points_for_purchase_date,
    points_for_purchase_time,
    points_from_retailer_name,
    points_if_total_is_a_multiple,
    points_if_total_is_round_dollar,
)


@pytest.mark.parametrize(
    "retailer_name, expected_points",
    [
        ("Walmart", 7),
        ("BestBuy123", 10),
        ("M&M Corner Market", 14),
        ("Whole-Foods Market", 16),
        ("A ", 1),
        ("Super-Store 2024", 14),
        ("Dollar & More", 10),
        ("The Fresh Market", 14),
        ("Shop & Save", 8),
        ("Test-Store_99", 11),
    ],
)
def test_points_from_retailer_name(retailer_name, expected_points):
    """
    Test that the points are correctly calculated based on alphanumeric
    characters in retailer name.
    """
    receipt = Receipt(
        retailer=retailer_name,
        purchaseDate="2022-03-20",
        purchaseTime="15:59",
        items=[{"shortDescription": "Gatorade", "price": "2.25"}],
        total="2.25",
    )
    assert points_from_retailer_name(receipt) == expected_points


@pytest.mark.parametrize(
    "total, expected_points",
    [
        ("9.00", 50),
        ("35.35", 0),
        ("50.01", 0),
        ("49.99", 0),
        ("0.00", 50),
    ],
)
def test_points_if_total_is_round_dollar(total, expected_points):
    """
    Test that the points are correctly calculated based on the total
    being a round number or not
    """
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-03-20",
        purchaseTime="15:59",
        items=[{"shortDescription": "Gatorade", "price": "2.25"}],
        total=total,
    )
    assert points_if_total_is_round_dollar(receipt) == expected_points


@pytest.mark.parametrize(
    "total, expected_points",
    [
        ("25.00", 25),
        ("0.25", 25),
        ("0.50", 25),
        ("0.75", 25),
        ("1.00", 25),
        ("59.99", 0),
        ("0.00", 25),
    ],
)
def test_points_if_total_is_a_multiple(total, expected_points):
    """
    Test that the points are correctly calculated based on the
    total being a round number or not
    """
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-03-20",
        purchaseTime="15:59",
        items=[{"shortDescription": "Gatorade", "price": "2.25"}],
        total=total,
    )
    assert points_if_total_is_a_multiple(receipt) == expected_points


@pytest.mark.parametrize(
    "item_list, expected_points",
    [
        (
            [{"shortDescription": "Gatorade", "price": "2.25"}],
            0,
        ),
        (
            [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
            ],
            5,
        ),
        (
            [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
            ],
            5,
        ),
        (
            [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
            ],
            15,
        ),
    ],
)
def test_points_for_item_list_count(item_list, expected_points):
    """
    Test that the points are correctly calculated based on the number of
    items in the receipt
    """
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-03-20",
        purchaseTime="15:59",
        items=item_list,
        total="100.00",
    )
    assert points_for_item_list_count(receipt) == expected_points


@pytest.mark.parametrize(
    "item_list, expected_points",
    [
        (
            [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"},
            ],
            6,
        ),
        (
            [
                {"shortDescription": "Egg", "price": "1.00"},
                {"shortDescription": "Orange", "price": "2.50"},
                {"shortDescription": "Klarbrunn 12PK", "price": "5.00"},
            ],
            2,
        ),
        (
            [
                {"shortDescription": "Samsung TV", "price": "999.99"},
                {"shortDescription": "   Juice Box   ", "price": "1.99"},
                {"shortDescription": "TV", "price": "299.99"},
            ],
            1,
        ),
        (
            [
                {"shortDescription": "   Fresh Banana   ", "price": "1.50"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            ],
            1,
        ),
        (
            [
                {"shortDescription": "   Super Sale Product  ", "price": "15.00"},
                {"shortDescription": "Discounted Soap", "price": "4.25"},
            ],
            4,
        ),
        (
            [
                {"shortDescription": "   ", "price": "15.00"},
            ],
            3,
        ),
        (
            [
                {"shortDescription": "   Item", "price": "15.00"},
            ],
            0,
        ),
    ],
)
def test_points_for_item_description(item_list, expected_points):
    """
    Test that the points are correctly calculated based on each item description
    """
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-03-20",
        purchaseTime="15:59",
        items=item_list,
        total="100.00",
    )
    assert points_for_item_description(receipt) == expected_points


@pytest.mark.parametrize(
    "purchase_date, expected_points",
    [
        ("2022-01-01", 6),
        ("2022-01-02", 0),
        ("2022-01-31", 6),
        ("2022-03-15", 6),
        ("2022-04-30", 0),
        ("2022-07-07", 6),
        ("2022-08-08", 0),
        ("2023-11-11", 6),
        ("2023-12-24", 0),
        ("2023-12-25", 6),
        ("2024-02-29", 6),
    ],
)
def test_points_for_purchase_date(purchase_date, expected_points):
    """
    Test that the points are correctly calculated based on the purchase date rule.
    """
    receipt = Receipt(
        retailer="Target",
        purchaseDate=purchase_date,
        purchaseTime="15:59",
        items=[{"shortDescription": "Gatorade", "price": "2.25"}],
        total="100.00",
    )
    assert points_for_purchase_date(receipt) == expected_points


@pytest.mark.parametrize(
    "purchase_time, expected_points",
    [
        ("14:33", 10),
        ("14:00", 0),
        ("14:01", 10),
        ("16:00", 0),
        ("15:59", 10),
        ("13:59", 0),
        ("16:01", 0),
        ("15:00", 10),
    ],
)
def test_points_for_purchase_time(purchase_time, expected_points):
    """
    Test that the points are correctly calculated based on the purchase time.
    """
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-01-01",
        purchaseTime=purchase_time,
        items=[{"shortDescription": "Gatorade", "price": "2.25"}],
        total="100.00",
    )
    assert points_for_purchase_time(receipt) == expected_points
