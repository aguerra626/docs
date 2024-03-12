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
##################################################################
##################################################################
##################################################################
##################################################################
##################################################################
##################################################################
import tableauserverclient as TSC
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

server_url = 'https://your-tableau-server'  # Replace with your Tableau server URL
site_id = 'your_site_id'  # Replace with your site ID, or use '' for the default site

# Set up Kerberos authentication
kerberos_auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)

# Set up Tableau Server connection
server = TSC.Server(server_url, use_server_version=True)

# Sign in
with server.auth.sign_in_with_http_auth(site_id=site_id, auth=kerberos_auth):
    # Perform your actions here
    # Example: List all workbooks
    all_workbooks, pagination_item = server.workbooks.get()
    for workbook in all_workbooks:
        print(workbook.name)

# Remember to replace 'your-tableau-server' and 'your_site_id' with your actual server and site ID.
########################################
########################################
########################################
########################################
########################################
import tableauserverclient as TSC

def tableau_list_workbooks_in_project(server_url, site_id, token_name, token_value, project_name):
    try:
        # Configure authentication with the personal access token
        personal_access_token_auth = TSC.PersonalAccessTokenAuth(token_name=token_name, personal_access_token=token_value, site_id=site_id)

        # Connect to the Tableau Server
        server = TSC.Server(server_url, use_server_version=True)

        with server.auth.sign_in_with_personal_access_token(personal_access_token_auth):
            print("Authentication successful!")
            
            # Find the project ID by name
            all_projects, _ = server.projects.get()
            project_id = None
            for project in all_projects:
                if project.name == project_name:
                    project_id = project.id
                    break

            if project_id is None:
                print(f"Project '{project_name}' not found.")
                return

            # List all workbooks in the specified project
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.ProjectId, TSC.RequestOptions.Operator.Equals, project_id))

            all_workbooks, _ = server.workbooks.get(req_options=req_option)
            print(f"Workbooks in project '{project_name}':")
            for workbook in all_workbooks:
                print(workbook.name)

    except TSC.ServerResponseError as e:
        print(f"Server response error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
server_url = 'https://your-tableau-server'  # Replace with your Tableau server URL
site_id = 'your_site_id'  # Replace with your site ID
token_name = 'your_token_name'  # Replace with your token name
token_value = 'your_token_value'  # Replace with your token value
project_name = 'Specific Project Name'  # Replace with the name of your project

tableau_list_workbooks_in_project(server_url, site_id, token_name, token_value, project_name)
