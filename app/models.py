from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ReceiptRequest(BaseModel):
    group: List[str] = Field(..., description="List of group member usernames")


class SplitItem(BaseModel):
    item_name: str = Field(..., description="Name of the item")
    total_cost: float = Field(..., description="Total cost of the item")
    cost_per_person: float = Field(..., description="Cost per person for this item")
    assigned_to: List[str] = Field(..., description="List of people assigned to this item")


class BillSplitResponse(BaseModel):
    restaurant_name: Optional[str] = Field(None, description="Name of the restaurant")
    total_amount: float = Field(..., description="Total bill amount")
    tax: float = Field(default=0.0, description="Tax amount")
    tip: float = Field(default=0.0, description="Tip amount")
    items: List[SplitItem] = Field(..., description="List of itemized splits")
    individual_totals: Dict[str, float] = Field(..., description="Total amount owed by each person")
    group_members: List[str] = Field(..., description="List of group members") 