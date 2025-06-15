import asyncio
from typing import Optional
import google.generativeai as genai
from PIL import Image
import io
from app.config import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiClient:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-pro-preview-06-05')
    
    async def extract_text_from_image(self, image_bytes: bytes) -> str:
        """Extract text from receipt image using Gemini Vision API"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Create the prompt for OCR
            prompt = """
            Please extract all text from this receipt image. 
            Include item names, prices, taxes, tips, and any other relevant information.
            Maintain the structure and formatting as much as possible.
            """
            
            # Run the model in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content([prompt, image])
            )
            
            return response.text if response.text else ""
            
        except Exception as e:
            raise Exception(f"Failed to extract text from image: {str(e)}")
    
    async def analyze_receipt_structure(self, image_bytes: bytes) -> str:
        """Analyze receipt structure and extract structured data"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            prompt = """
            Analyze this receipt image and extract the following information in a structured format:
            - Restaurant/establishment name
            - Individual items with names and prices
            - Subtotal, tax, tip, and total amounts
            - Any special offers or discounts
            
            Format the response as clear, structured text that can be easily parsed.
            """
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content([prompt, image])
            )
            
            return response.text if response.text else ""
            
        except Exception as e:
            raise Exception(f"Failed to analyze receipt structure: {str(e)}")


# Global client instance
gemini_client = GeminiClient() 