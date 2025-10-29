from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Dict, Any

load_dotenv()

class NLtoSQL:
    def __init__(self):
        # Initialize OpenAI client with API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)

    def generate_sql(self, natural_language_query: str) -> str:
        """
        Convert natural language query to SQL using OpenAI's API
        """
        try:
            # Create a prompt that guides the model to generate SQL
            prompt = f"""Given the following natural language query, generate a valid SQL query.
            Only generate SELECT queries for security reasons.
            Natural language query: {natural_language_query}
            
            Return only the SQL query, nothing else."""

            # Generate SQL query using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a SQL expert. Generate only SELECT queries. No explanations, just the SQL query."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1  # Lower temperature for more deterministic output
            )
            

            #test   
            # Extract SQL query from response
            sql_query = response.choices[0].message.content.strip().rstrip(';')
            
            # Validate query type
            if not sql_query.lower().startswith('select'):
                raise ValueError("Only SELECT queries are allowed for security reasons")
            
            return sql_query
        except Exception as e:
            raise Exception(f"Error generating SQL query: {str(e)}")