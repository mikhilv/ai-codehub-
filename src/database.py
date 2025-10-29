import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

class SnowflakeDB:
    def __init__(self):
        self.conn = snowflake.connector.connect(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )

    def execute_query(self, query: str) -> list:
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            
            # Convert results to list of dictionaries
            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")

    def close(self):
        if self.conn:
            self.conn.close()