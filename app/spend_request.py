from pydantic import BaseModel


class SpendRequest(BaseModel):
    points: int