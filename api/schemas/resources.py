from pydantic import BaseModel
from typing import Optional


class ResourceBase(BaseModel):
    name: str
    amount: float
    unit: str  # Unit of measurement (e.g., kg, liter, etc.)


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float]  = None
    unit: Optional[str] = None


class Resource(ResourceBase):
    id: int

    class ConfigDict:
        from_attributes = True
