# MCP Server for Natural Language SQL Queries

This project implements a Model Context Protocol (MCP) server that accepts natural language queries, converts them to SQL using machine learning, executes them on a SnowSQL database, and returns the results in JSON format.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure your SnowSQL connection:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your SnowSQL credentials

## Running the Server

To run the server:

```bash
uvicorn src.server:app --reload
```

The server will start on `http://localhost:8000`

## API Usage

### POST /query

Send natural language queries to get SQL results.

Request body:
```json
{
    "query": "Show me all sales from last month"
}
```

Response:
```json
{
    "sql_query": "SELECT * FROM sales WHERE date >= DATEADD(month, -1, CURRENT_DATE())",
    "results": [
        {
            "sale_id": 1,
            "amount": 100.50,
            "date": "2023-09-15"
        }
        // ... more results
    ]
}
```

## Security Notes

- The server only allows SELECT queries for security reasons
- Make sure to properly configure your SnowSQL user permissions
- Keep your .env file secure and never commit it to version control

## Error Handling

The server provides detailed error messages for:
- Invalid natural language queries
- SQL generation failures
- Database connection issues
- Query execution errors