from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from config import auth as config_auth
import json
import sys

auth = v3.Password(**config_auth)
sess = session.Session(auth=auth)
keystone = client.Client(session=sess)

def create_project(name, description='', domain='default', enabled=True):
    try:
        project = keystone.projects.create(name=name,
                                           description=description,
                                           domain=domain,
                                           enabled=enabled)
    except Exception:
        return None

    print('project %s created' % name)
    return project

def create_user(name, default_project, domain='default'):
    try:
        user = keystone.users.create(name=name,
                                     domain=domain,
                                     password=name,
                                     default_project=default_project)
    except Exception:
        return None

    print('user %s created' % name)
    return user

def create_projects(project_names):
    for project_name in project_names:
        create_project(project_name)

def create_project_users(project_name, user_names):
    project = next(project for project in keystone.projects.list() \
                   if project.name == project_name)

    member_role = next(role for role in keystone.roles.list() \
                       if role.name == '_member_')
    superadmin_role = next(role for role in keystone.roles.list() \
                       if role.name == 'superadmin')
    admin_role = next(role for role in keystone.roles.list() \
                       if role.name == 'admin')


    for idx, user_name in enumerate(user_names):
        user = create_user(user_name, project)
        try:
            keystone.roles.grant(role=member_role, user=user, \
                                 project=project)
            if idx == 0:
                keystone.roles.grant(role=superadmin_role, user=user, \
                                     project=project)
                keystone.roles.grant(role=admin_role, user=user, \
                                     project=project)

        except Exception:
            continue

try:
    file_name = sys.argv[1] or 'list.json'
except Exception:
    file_name = 'list.json'

with open(file_name) as data_file:
    data = json.load(data_file)

create_projects(data.keys())

for project_name, user_names in data.items():
    create_project_users(project_name, user_names)
