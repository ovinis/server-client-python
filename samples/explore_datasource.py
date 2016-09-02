####
# This script demonstrates how to use the Tableau Server API
# to interact with datasources. It explores the different
# functions that the Server API supports on datasources.
#
# With no flags set, this sample will query all datasources,
# pick one datasource and populate its connections, and update
# the datasource. Adding flags will demonstrate the specific feature
# on top of the general operations.
####


import tableauserverapi as TSA
import os.path
import argparse
import logging

parser = argparse.ArgumentParser(description='Explore datasource functions supported by the Server API.')
parser.add_argument('server', help='server address')
parser.add_argument('username', help='username to sign into server')
parser.add_argument('password', help='password to sign into server')
parser.add_argument('-info', action='store_true', help='set this flag to show logging information on INFO level')
parser.add_argument('-debug', action='store_true', help='set this flag to show logging information on DEBUG level')
parser.add_argument('-publish', '-p', metavar='FILEPATH', help='path to datasource to publish')
parser.add_argument('-download', '-d', metavar='FILEPATH', help='path to save downloaded datasource')
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
elif args.info:
    logging.basicConfig(level=logging.INFO)

##### SIGN IN #####
tableau_auth = TSA.TableauAuth(args.username, args.password)
server = TSA.Server(args.server)
with server.auth.sign_in(tableau_auth):

    # Query projects for use when demonstrating publishing and updating
    pagination_item, all_projects = server.projects.get()
    default_project = next((project for project in all_projects if project.is_default()), None)

    # Publish datasource if publish flag is set (-publish, -p)
    if args.publish:
        if default_project is not None:
            new_datasource = TSA.DatasourceItem(default_project.id)
            new_datasource = server.datasources.publish(new_datasource, args.publish, server.PublishMode.Overwrite)
            print("Datasource published. ID: {}".format(new_datasource.id))
        else:
            print("Publish failed. Could not find the default project.")

    # Gets all datasource items
    pagination_item, all_datasources = server.datasources.get()
    print("\nThere are {} datasources on site: ".format(pagination_item.total_available))
    print([datasource.name for datasource in all_datasources])

    if all_datasources:
        # Pick one datasource from the list
        sample_datasource = all_datasources[0]

        # Populate connections
        server.datasources.populate_connections(sample_datasource)
        print("\nConnections for datasource: ")
        print(["{0}({1})".format(connection.id, connection.datasource_name)
               for connection in sample_datasource.connections])










