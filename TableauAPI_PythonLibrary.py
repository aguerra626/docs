import tableauserverclient as TSC

def main():
    # Tableau Server or Online credentials and site details
    username = 'your_username'
    password = 'your_password'
    site_id = 'your_site_id'  # Use '' for default site
    server_url = 'https://your-tableau-server'

    # Connect to Tableau
    tableau_auth = TSC.TableauAuth(username, password, site_id)
    server = TSC.Server(server_url)

    with server.auth.sign_in(tableau_auth):
        # List all workbooks
        all_workbooks, pagination_item = server.workbooks.get()
        print("List of Workbooks:")
        for workbook in all_workbooks:
            print(workbook.name)

        # Download a workbook
        workbook_id = 'your-workbook-id'  # Replace with your workbook ID
        server.workbooks.download(workbook_id, filepath='workbook.twbx')

        # Publish a workbook
        new_workbook = TSC.WorkbookItem(project_id='your-project-id')
        server.workbooks.publish(new_workbook, 'path/to/workbook.twbx', 'Overwrite')

        # List all users
        all_users, pagination_item = server.users.get()
        print("\nList of Users:")
        for user in all_users:
            print(user.name)

        # Create a new user
        new_user = TSC.UserItem('new_username', TSC.UserItem.Roles.Viewer)
        server.users.add(new_user)

        # Delete a workbook
        server.workbooks.delete(workbook_id)

        # Query Data Sources
        all_datasources, pagination_item = server.datasources.get()
        print("\nList of Data Sources:")
        for datasource in all_datasources:
            print(datasource.name)

        # Update Site details
        site = server.sites.get_by_id(site_id)
        site.name = 'New Site Name'
        server.sites.update(site)

if __name__ == "__main__":
    main()