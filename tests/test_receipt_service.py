import pytest

from app.models import Receipt
from app.services.receipt_service import (
    points_for_item_list_count,
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
    Test that the points are correctly calculated based on alphanumeric characters in retailer name.
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
    Test that the points are correctly calculated based on the total being a round number or not
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
    Test that the points are correctly calculated based on the total being a round number or not
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
    Test that the points are correctly calculated based on the total being a round number or not
    """
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-03-20",
        purchaseTime="15:59",
        items=item_list,
        total="100.00",
    )
    assert points_for_item_list_count(receipt) == expected_points
