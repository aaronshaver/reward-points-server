from pydantic import BaseModel


class Transaction(BaseModel):
    payer_name: str
    points: int
    timestamp: str