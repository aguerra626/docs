import requests
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# Function to get data from Tableau API
def get_data_from_tableau(server, token, graphql_query):
    url = f"{server}/api/metadata/graphql"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Tableau-Auth': token
    }
    response = requests.post(url, json={'query': graphql_query}, headers=headers)
    return response.json()

# Example usage - replace these with your actual details
SERVER_URL = "https://your-tableau-server.com"
TOKEN = "your-access-token"

# Example GraphQL query to fetch data (modify according to your needs)
graphql_query = """
{
  # Your GraphQL query here
}
"""

tableau_data = get_data_from_tableau(SERVER_URL, TOKEN, graphql_query)

# Convert Tableau data to Pandas DataFrame (modify according to your data structure)
df = pd.DataFrame(tableau_data['data'])

# Connect to SQL Server
# Replace with your SQL Server connection details
sql_server = 'server_name'
database = 'database_name'
username = 'username'
password = 'password'

connection_string = f"mssql+pyodbc://{username}:{password}@{sql_server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string)

# Import data into SQL Server
# Replace 'your_table_name' with your actual table name
table_name = 'your_table_name'

df.to_sql(table_name, engine, if_exists='append', index=False, method='multi', chunksize=1000)