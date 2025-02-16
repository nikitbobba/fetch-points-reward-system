import math

from app.models import Receipt


def calculate_points(receipt: Receipt) -> int:
    """
    Should calculate the total number of points for a given receipt
    based on all the rules

    Args:
        receipt: Receipt object

    Returns:
        int: Total number of points
    """

    rules = [
        points_from_retailer_name,
        points_if_total_is_round_dollar,
        points_if_total_is_a_multiple,
        points_for_item_list_count,
        points_for_item_description,
        points_for_purchase_date,
        points_for_purchase_time,
    ]

    return sum(rule(receipt) for rule in rules)


def points_from_retailer_name(receipt: Receipt) -> int:
    """
    Should return one point for every alphanumeric character in the retailer name.

    Args:
        receipt: Receipt object

    Returns:
        int: number of points
    """
    points = sum(1 for c in receipt.retailer if c.isalnum())
    print("points_from_retailer_name: ", points)
    return points


def points_if_total_is_round_dollar(receipt: Receipt) -> int:
    """
    Should return 50 points if the total is a round dollar amount with no cents.

    Args:
        receipt: Receipt object

    Returns:
        int: number of points
    """
    points = 50 if receipt.total.endswith(".00") else 0
    print("points_if_total_is_round_dollar: ", points)
    return points


def points_if_total_is_a_multiple(receipt: Receipt) -> int:
    """
    Should return 25 points if the total is a multiple of 0.25.

    Args:
        receipt: Receipt object

    Returns:
        int: number of points
    """
    points = 25 if float(receipt.total) % 0.25 == 0 else 0
    print("points_if_total_is_a_multiple: ", points)
    return points


def points_for_item_list_count(receipt: Receipt) -> int:
    """
    Should return 5 points for every two items in the receipt.

    Args:
        receipt: Receipt object

    Returns:
        int: number of points
    """
    points = (len(receipt.items) // 2) * 5
    print("points_for_item_list_count: ", points)
    return points


def points_for_item_description(receipt: Receipt) -> int:
    """
    If the trimmed length of the item description is a multiple of 3,
    multiply the price by 0.2 and round up to the nearest integer.
    The result is the number of points earned for a single item.

    Args:
        receipt: Receipt object

    Returns:
        int: number of points
    """
    totalItemPoints = 0
    for item in receipt.items:
        trimmed_length = len(
            item.short_description.strip()
        )  # Trim spaces and get length
        if trimmed_length % 3 == 0:  # Check if it's a multiple of 3
            totalItemPoints += math.ceil(
                float(item.price) * 0.2
            )  # Multiply by 0.2 and round up

    print("points_for_item_description: ", totalItemPoints)
    return totalItemPoints


def points_for_purchase_date(receipt: Receipt) -> int:
    """
    Should return 6 points if the day in the purchase date of the receipt is odd.

    Args:
        receipt: Receipt object

    Returns:
        int: number of points
    """
    points = 6 if receipt.purchase_date.day % 2 != 0 else 0
    print("points_for_purchase_date: ", points)
    return points


def points_for_purchase_time(receipt: Receipt) -> int:
    """
    Should return 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    I'm making the assumption that it is a non inclusive date range here

    Args:
        receipt: Receipt object

    Returns:
        int: number of points
    """
    purchase_hour = receipt.purchase_time.hour
    purchase_minute = receipt.purchase_time.minute

    purchase_time_in_minutes = (purchase_hour * 60) + purchase_minute

    # Using 2:01 and 3:59 as the inclusive boundaries
    start_time = (14 * 60) + 1
    end_time = 16 * 60

    points = 10 if start_time <= purchase_time_in_minutes < end_time else 0

    print(f"Purchase time: {receipt.purchase_time}, Points awarded: {points}")
    return points
