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






import requests
import json

# Tableau Server details and personal access token
server_url = 'https://your-tableau-server'  # Replace with your Tableau server URL
api_version = '3.13'  # Use the API version supported by your server
site_name = 'your_site_name'  # Replace with your site name
token_name = 'your_token_name'  # Replace with your token name
token_value = 'your_token_value'  # Replace with your token value

# Authentication endpoint
auth_url = f"{server_url}/api/{api_version}/auth/signin"

# Headers and payload for authentication
headers = {
    'Content-Type': 'application/json',
}
payload = {
    "credentials": {
        "personalAccessTokenName": token_name,
        "personalAccessTokenSecret": token_value,
        "site": {
            "contentUrl": site_name
        }
    }
}

# Start a session and authenticate
with requests.Session() as session:
    response = session.post(auth_url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print("Authentication failed")
        exit()

    # Extract the token from the response
    token = response.json()['credentials']['token']
    headers['X-Tableau-Auth'] = token

    # List all projects
    projects_url = f"{server_url}/api/{api_version}/sites/{site_name}/projects"
    response = session.get(projects_url, headers=headers)

    if response.status_code == 200:
        projects = response.json()['projects']['project']
        print("Projects and IDs:")
        for project in projects:
            print(f"{project['name']} - ID: {project['id']}")
    else:
        print("Failed to retrieve projects")

    # List all workbooks
    workbooks_url = f"{server_url}/api/{api_version}/sites/{site_name}/workbooks"
    response = session.get(workbooks_url, headers=headers)

    if response.status_code == 200:
        workbooks = response.json()['workbooks']['workbook']
        print("\nWorkbooks:")
        for workbook in workbooks:
            print(workbook['name'])
    else:
        print("Failed to retrieve workbooks")
########################################
########################################
########################################
########################################
########################################
import tableauserverclient as TSC

# Step 1: Connect to Tableau Server using your personal access token
tableau_auth = TSC.PersonalAccessTokenAuth(token_name='YOUR_TOKEN_NAME',
                                           personal_access_token='YOUR_PERSONAL_ACCESS_TOKEN',
                                           site_id='YOUR_SITE_ID')
server = TSC.Server('https://YOUR_TABLEAU_SERVER_URL', use_server_version=True)

# Step 2: Sign in to server
with server.auth.sign_in(tableau_auth):
    # Step 3: Check connection status
    print(f"Connected to Tableau Server: {server.is_signed_in()}")

    # Step 4: Get the project by its ID
    project_id = 'YOUR_PROJECT_ID'
    project = server.projects.get_by_id(project_id)

    if project is None:
        print(f"Project with ID '{project_id}' not found.")
    else:
        # Step 5: List all workbooks in the project
        print(f"Workbooks in the project '{project.name}':")
        for workbook in project.workbooks:
            print(f"- {workbook.name}")

        # Step 6: Get total view counts for each workbook and store in a dictionary
        workbook_view_counts = {}
        for workbook in project.workbooks:
            total_view_count = sum(view.total_view_count for view in workbook.views)
            workbook_view_counts[workbook.name] = total_view_count

        # Step 7: Print the workbook view counts dictionary
        print("Total view counts per workbook:")
        for workbook_name, view_count in workbook_view_counts.items():
            print(f"'{workbook_name}': {view_count}")

from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils.querying import get_projects_dataframe

# Define your connection details
connection_details = {
    'server': 'https://YOUR-SERVER-URL',
    'username': 'YOUR_USERNAME',
    'password': 'YOUR_PASSWORD',
    'site_name': 'YOUR_SITE_NAME',  # Leave blank for default site
    'site_url': 'YOUR_SITE_URL'  # This is part of your Tableau URL, often it's the site name
}

# Create a connection object
conn = TableauServerConnection(**connection_details)

# Sign in to Tableau Server
conn.sign_in()

# Now you can perform various actions, for example, getting a list of projects
projects_df = get_projects_dataframe(conn)

# Always remember to sign out when you're done
conn.sign_out()

from tableau_api_lib import TableauServerConnection
from tableau_api_lib.exceptions import PaginationError
from tableau_api_lib.utils.querying import get_projects_dataframe
import json

# Define your connection details
connection_details = {
    'tableau_prod': {
        'server': 'https://YOUR-SERVER-URL',
        'username': 'YOUR_USERNAME',
        'password': 'YOUR_PASSWORD',
        'site_name': 'YOUR_SITE_NAME',  # Leave blank for default site
        'site_url': 'YOUR_SITE_URL'  # This is part of your Tableau URL, often it's the site name
    }
}

# Create a connection object
conn = TableauServerConnection(**connection_details['tableau_prod'])

try:
    # Sign in to Tableau Server
    conn.sign_in()

    # Perform actions, for example, getting a list of projects
    projects_df = get_projects_dataframe(conn)
    print(projects_df)

except PaginationError as e:
    print("PaginationError occurred: ", e)
    # Handle pagination-specific issues here

except json.JSONDecodeError as e:
    print("JSONDecodeError occurred: ", e)

except Exception as e:
    print("An error occurred: ", e)

finally:
    # Always remember to sign out when you're done
    conn.sign_out()


import tableauserverclient as TSC

# ... (setup your server connection and authentication here)

# Fetching all views and printing their total views count
try:
    with server.auth.sign_in(tableau_auth):
        all_views = TSC.Pager(server.views.get)
        for view in all_views:
            # You may need to populate specific properties if they're not automatically included
            server.views.populate_usage_statistics(view)
            print(f"View: {view.name}, Total Views: {view.total_views_count}")
except Exception as e:
    print(f"An error occurred: {e}")

