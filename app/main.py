from fastapi import FastAPI

from app.routers import receipts

app = FastAPI()

app.include_router(receipts.router)
