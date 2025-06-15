from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
import json

from app.models import BillSplitResponse
from app.chains.receipt_split import receipt_split_chain

router = APIRouter(prefix="/receipts", tags=["receipts"])


@router.post("/split", response_model=BillSplitResponse)
async def split_receipt(
    image: UploadFile = File(..., description="Receipt image file"),
    group: str = Form(..., description="JSON string of group member usernames")
) -> BillSplitResponse:
    """
    Split a receipt among group members.
    
    Args:
        image: The receipt image file (PNG, JPG, JPEG)
        group: JSON string containing list of group member usernames
    
    Returns:
        BillSplitResponse: Detailed bill split with individual amounts
    """
    try:
        # Validate file type
        if not image.content_type or not image.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail="File must be an image (PNG, JPG, JPEG)"
            )
        
        # Parse group list from JSON string
        try:
            group_list = json.loads(group)
            if not isinstance(group_list, list) or not all(isinstance(member, str) for member in group_list):
                raise ValueError("Group must be a list of strings")
            if len(group_list) == 0:
                raise ValueError("Group must contain at least one member")
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid group format: {str(e)}. Expected JSON array of strings."
            )
        
        # Read image bytes without saving to disk
        image_bytes = await image.read()
        
        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty image file"
            )
        
        # Validate image size (10MB limit)
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Image file too large. Maximum size is 10MB."
            )
        
        # Process the receipt using LangChain
        result = await receipt_split_chain.split_receipt(image_bytes, group_list)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process receipt: {str(e)}"
        )


@router.get("/health")
async def receipts_health():
    """Health check endpoint for receipts service"""
    return {"status": "ok", "service": "receipts"} 