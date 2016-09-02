import json
from keystoneclient.v3 import client
from config import auth as config_auth
from keystoneauth1.identity import v3
from keystoneauth1 import session
import sys

try:
    file_name = sys.argv[1] or 'list.json'
except Exception:
    file_name = 'list.json'

with open(file_name) as data_file:
    data = json.load(data_file)

auth = v3.Password(**config_auth)
sess = session.Session(auth=auth)
keystone = client.Client(session=sess)

user_names = [user_name for project_user in data.values() for user_name in project_user]

project_names = data.keys()

def delete_users(user_names):
    online_users = keystone.users.list()

    for online_user in online_users:
        if online_user.name in user_names:
            try:
                keystone.users.delete(online_user)
            except Exception:
                continue
            print('user %s deleted' % online_user.name)
def delete_projects(project_names):
    online_projects = keystone.projects.list()
    for online_project in online_projects:
        if online_project.name in project_names:
            try:
                keystone.projects.delete(online_project)
            except Exception:
                continue
            print('project %s deleted' % online_project.name)

delete_users(user_names)
delete_projects(project_names)
