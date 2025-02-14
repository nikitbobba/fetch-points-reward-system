from fastapi.testclient import TestClient

from app.main import app  # Import FastAPI app

client = TestClient(app)


def test_process_receipt():
    """
    Verify POST process_receipt returns a 200 with a valid input body
    """
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"},
        ],
        "total": "35.35",
    }

    response = client.post("/receipts/process", json=receipt_data)
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_receipt_points():
    """
    Verify the GET /receipts/{id}/points endpoint returns the total number of points
    """
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"},
        ],
        "total": "35.35",
    }

    response = client.post("/receipts/process", json=receipt_data)
    receipt_id = response.json()["id"]

    # Now, fetch the points
    response = client.get(f"/receipts/{receipt_id}/points")
    assert response.status_code == 200
    assert "points" in response.json()
    assert response.json()["points"] == 28


def test_receipt_not_found():
    """Test GET /receipts/{id}/points for an invalid receipt ID"""
    response = client.get("/receipts/nonexistent-id/points")
    assert response.status_code == 404
    assert response.json() == {"detail": "No receipt found for that ID."}
