# Receipt Splitter API

An async FastAPI backend that implements in-memory receipt uploads, Gemini AI integration, and LangChain orchestration for intelligent bill splitting.

## Features

- 🚀 **Async FastAPI Backend** - High-performance asynchronous API
- 🤖 **Gemini AI Integration** - Advanced OCR and text extraction from receipt images
- 🔗 **LangChain Orchestration** - Intelligent prompting, parsing, and error handling
- 💰 **Smart Bill Splitting** - Automatically split bills among group members
- 📱 **In-Memory Processing** - No file storage, all processing done in memory
- 🔒 **Type Safety** - Full TypeScript-style typing with Pydantic models
- 📊 **Structured Output** - JSON responses with detailed split information

## Project Structure

```
app/
├── __init__.py                 # Package initialization
├── main.py                     # FastAPI application entry point
├── config.py                   # Environment configuration
├── models.py                   # Pydantic data models
├── chains/
│   └── receipt_split.py        # LangChain integration for bill splitting
├── routes/
│   └── receipts.py            # Receipt processing endpoints
└── utils/
    └── gemini_client.py       # Gemini AI client utilities
requirements.txt               # Python dependencies
README.md                     # This file
```

## Prerequisites

- Python 3.8+
- Google Gemini API key

## Installation

1. **Clone or create the project directory:**
   ```bash
   mkdir receipt-splitter-api
   cd receipt-splitter-api
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Get a Gemini API key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the API key

2. **Set environment variables:**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   Or set the environment variable directly:
   ```bash
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```http
GET /health
```
Returns the API health status.

### Split Receipt
```http
POST /receipts/split
```

**Parameters:**
- `image` (file): Receipt image (PNG, JPG, JPEG, max 10MB)
- `group` (form field): JSON string array of group member usernames

**Example:**
```bash
curl -X POST "http://localhost:8000/receipts/split" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@receipt.jpg" \
  -F 'group=["alice", "bob", "charlie"]'
```

**Response:**
```json
{
  "restaurant_name": "The Great Restaurant",
  "total_amount": 45.50,
  "tax": 3.64,
  "tip": 9.10,
  "items": [
    {
      "item_name": "Burger",
      "total_cost": 15.99,
      "cost_per_person": 5.33,
      "assigned_to": ["alice", "bob", "charlie"]
    }
  ],
  "individual_totals": {
    "alice": 15.17,
    "bob": 15.17,
    "charlie": 15.16
  },
  "group_members": ["alice", "bob", "charlie"]
}
```

## Data Models

### ReceiptRequest
```python
{
  "group": ["string"]  # List of group member usernames
}
```

### BillSplitResponse
```python
{
  "restaurant_name": "string",      # Restaurant name (optional)
  "total_amount": 0.0,             # Total bill amount
  "tax": 0.0,                      # Tax amount
  "tip": 0.0,                      # Tip amount
  "items": [SplitItem],            # List of itemized splits
  "individual_totals": {},         # Amount owed by each person
  "group_members": ["string"]      # List of group members
}
```

### SplitItem
```python
{
  "item_name": "string",           # Name of the item
  "total_cost": 0.0,              # Total cost of the item
  "cost_per_person": 0.0,         # Cost per person for this item
  "assigned_to": ["string"]       # List of people assigned to this item
}
```

## Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - Lightning-fast ASGI server
- **Pydantic** - Data validation using Python type annotations
- **Google Generative AI** - Gemini AI integration for OCR and text processing
- **LangChain** - Framework for developing applications with LLMs
- **Pillow** - Python Imaging Library for image processing
- **Python-multipart** - For handling multipart/form-data requests

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting
```bash
# Install formatting tools
pip install black isort

# Format code
black .
isort .
```

### Type Checking
```bash
# Install mypy
pip install mypy

# Run type checking
mypy app/
```

## Deployment

### Using Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production
- `GEMINI_API_KEY` - Your Gemini API key (required)
- `HOST` - Host to bind to (default: 0.0.0.0)
- `PORT` - Port to bind to (default: 8000)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the repository or contact the development team.

---

**Note**: This API processes images in memory and does not store any uploaded files on disk. All processing is ephemeral and secure. 