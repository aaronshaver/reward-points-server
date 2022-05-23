from pydantic import BaseModel


class Transaction(BaseModel):
    payer: str
    points: int
    timestamp: str