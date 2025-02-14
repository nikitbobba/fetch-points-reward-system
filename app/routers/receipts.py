import uuid

from fastapi import APIRouter, HTTPException

from app.models import GetReceiptPointsResponse, ProcessReceiptResponse, Receipt
from app.services.receipt_service import calculate_points

router = APIRouter()

# Mocking an in memory database to store the uuid -> number of points
db: dict[str, int] = {}


@router.post(
    "/receipts/process",
    response_model=ProcessReceiptResponse,
    responses={400: {"description": "The receipt is invalid."}},
    summary="Submits a receipt for processing.",
    description="Submits a receipt for processing.",
)
def process_receipt(receipt: Receipt):
    """
    Given a receipt, calculate the total number of points for it
    and save it in the db

    Args:
        receipt (Receipt): the Receipt body

    Returns:
        ProcessReceiptResponse: A uniqueId to fetch the points for the receipt

    Raises:
        HTTPException(400): If the input has malformed values
    """
    totalPoints = calculate_points(receipt)
    receiptId = str(uuid.uuid4())
    db[receiptId] = totalPoints
    print(f"Saved receiptId: ${receiptId} with total points: ${totalPoints} to db")
    return ProcessReceiptResponse(id=receiptId)


@router.get(
    "/receipts/{receipt_id}/points",
    response_model=GetReceiptPointsResponse,
    responses={404: {"description": "No receipt found for that ID."}},
    summary="Returns the points awarded for the receipt.",
    description="Returns the points awarded for the receipt.",
)
def get_receipt_points(receipt_id: str):
    """
    Given a receiptId, return the points for it if it exists in the db
    Otherwise, throw a 404 NotFound exception

    Args:
        receipt_id (str): The ID of the receipt.

    Returns:
        GetReceiptPointsResponse: A JSON object containing the points awarded.

    Raises:
        HTTPException(404): If the receipt ID is not found.
    """
    if receipt_id in db:
        return GetReceiptPointsResponse(points=db[receipt_id])

    raise HTTPException(status_code=404, detail="No receipt found for that ID.")
