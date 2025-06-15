import asyncio
from typing import List
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import OutputParserException

from app.models import BillSplitResponse
from app.config import settings
from app.utils.gemini_client import gemini_client


class ReceiptSplitChain:
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro-preview-06-05",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.1
        )
        
        # Initialize the output parser
        self.output_parser = PydanticOutputParser(pydantic_object=BillSplitResponse)
        
        # Create the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["receipt_text", "group"],
            template="""
            You are a helpful assistant that analyzes receipts and splits bills among group members.
            
            This is a bill receipt: {receipt_text}
            
            The group members are: {group}
            
            Please extract itemized bill data and split each item, tax, and tip equally among group members.
            
            Instructions:
            1. Identify all individual items with their prices
            2. Calculate tax and tip amounts
            3. Split each item cost equally among all group members
            4. Calculate individual totals for each person
            5. Ensure all costs add up correctly
            
            {format_instructions}
            
            Return only the valid JSON response matching the BillSplitResponse schema.
            """,
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        
        # Create the chain
        self.chain = (
            RunnablePassthrough() 
            | self.prompt_template 
            | self.llm 
            | self.output_parser
        )
    
    async def split_receipt(self, image_bytes: bytes, group: List[str]) -> BillSplitResponse:
        """
        Process receipt image and split the bill among group members
        """
        try:
            # Extract text from the receipt image using Gemini Vision
            receipt_text = await gemini_client.analyze_receipt_structure(image_bytes)
            
            if not receipt_text:
                raise ValueError("Could not extract text from the receipt image")
            
            # Prepare input for the chain
            chain_input = {
                "receipt_text": receipt_text,
                "group": ", ".join(group)
            }
            
            # Run the chain asynchronously
            result = await self.chain.ainvoke(chain_input)
            
            # Ensure group members are set correctly
            if isinstance(result, BillSplitResponse):
                result.group_members = group
                return result
            else:
                raise ValueError("Invalid response format from LLM")
                
        except OutputParserException as e:
            # If parsing fails, try to create a basic response
            receipt_text = await gemini_client.extract_text_from_image(image_bytes)
            return self._create_fallback_response(receipt_text, group)
        
        except Exception as e:
            raise Exception(f"Failed to split receipt: {str(e)}")
    
    def _create_fallback_response(self, receipt_text: str, group: List[str]) -> BillSplitResponse:
        """Create a basic fallback response when parsing fails"""
        # This is a simple fallback - in production, you might want more sophisticated parsing
        total_per_person = 0.0
        individual_totals = {member: total_per_person for member in group}
        
        return BillSplitResponse(
            restaurant_name="Unknown Restaurant",
            total_amount=0.0,
            tax=0.0,
            tip=0.0,
            items=[],
            individual_totals=individual_totals,
            group_members=group
        )


# Global chain instance
receipt_split_chain = ReceiptSplitChain() 