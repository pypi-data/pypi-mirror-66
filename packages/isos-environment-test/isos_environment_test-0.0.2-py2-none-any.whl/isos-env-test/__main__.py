#!/usr/bin/env python3

# IIIIII  SSSS  OOOOO  SSSS     Isos Technology
#   II    S     O   O  S        https://www.isostech.com/
#   II    SSSS  O   O  SSSS     April 2020
#   II       S  O   O     S     sky.moore@isostech.com
# IIIIII  SSSS  OOOOO  SSSS

try:

    imports = True

    import requests
    import pickle
    from os import listdir
    from pathlib import Path, PurePath
    from getpass import getpass
    from atlassian import Jira
    from consolemenu import SelectionMenu
    from .credentials import auth_dict
    from .vars import username, api_token, url, param_pickle, creds_dict
    from .vars import site_unav_error, atl_error, remote_file, cloud

    print('\n\n\nImports successful, this environment works!\n\n')

except Exception as e:

    imports = False

    print('\n\n\nUnable to import necessary packages, see the following error:\n\n\n', e, '\n\n')


def jiraTest(auth_dict):
    try:
        jira = Jira(url=auth_dict[url], username=auth_dict[username],
                    password=auth_dict[api_token], cloud=auth_dict[cloud])
        projects = jira.projects(included_archived=False)
    except Exception as e:
        print("\n\n", e, "\n\n")
        exit(1)

    if isinstance(projects, str):
        print(
            f'Looks like you used your real password or made an error entering your api token...\n\nHere\'s Atlassian\'s message: \n\n{projects}')
    elif isinstance(projects, list):
        if len(projects) == 0:
            print("Jira Cloud access test failure, projects list is empty.\n\nDouble check your Url, Username, and API Token. Ensure that there is at least one project visible to the user you're authenticating as.\n\n")
            exit(1)
        else:
            print(
                f'\n\nJira Cloud access test successful, authenticated to {auth_dict[url]} and found {len(projects)} active projects.\n\n')
    elif isinstance(projects, dict):
        if atl_error in projects:
            if projects[atl_error] == site_unav_error:
                print(
                    f'\n\nGetting \'{site_unav_error}\' it\'s likely your URL is wrong.\n\n')
    else:
        print("something went wrong...\n\nHere\'s what I've got:\n\n", projects)
        exit(1)


def accessTest(auth_dict):
    try:
        path = Path(auth_dict[remote_file])
        path = path.resolve(strict=True)
        if path.exists():
            if path.is_dir():
                print(f'Can see that {path} exists and is a directory.\n')
                listdir(path)
                print(f'Successfully listed the contents of {path}\n')
            elif path.is_file():
                print(f'Can see that {path} exists and is a file.\n')
                with path.open('r') as a_file:
                    a_file.readline()
                    print(f'Successfully read the first line from {path}\n')
            else:
                print(f'Error attempting to access {path}')
        print(f'Successfully accessed {auth_dict[remote_file]}\n\n')
    except Exception as e:
        print(f'Error attempting to access {auth_dict[remote_file]}\n\n', e)


def updateThis(auth_dict, key, title=None):

    if not title:
        title = 'Parameter: ' + creds_dict[key]

    option = SelectionMenu.get_selection(
        ['Keep', 'Update'],
        title=title,
        subtitle=f'Current {creds_dict[key]}: {auth_dict[key]}\n\n\tWhat would you like to do?')

    if key == api_token:
        update_funtion = getpass
    else:
        update_funtion = input

    if option == 0:
        pass
    elif option == 1:
        auth_dict[key] = update_funtion(
            f'Please enter a new value for {creds_dict[key]}: ')
    else:
        print('\n\nAborting all changes...\n\n')
        exit(0)


def updateParameters(path, auth_dict):
    for cred in creds_dict:
        updateThis(auth_dict, cred)

    try:
        with open(path, 'wb') as pickled_parameters:
            pickle.dump(auth_dict, pickled_parameters)
    except Exception as e:
        print("There was an error trying to update your parameters cache: ", e, "\n\n")
        exit(1)

    userParameters()


def userParameters():

    try:
        with open(param_pickle, 'rb') as pickled_parameters:
            p_auth_dict = pickle.load(pickled_parameters)
    except Exception as e:
        print("There was an error trying to read your parameters cache: ", e, "\n\n")
        exit(1)

    option = SelectionMenu.get_selection(
        ['Use these parameters', 'Update these parameters'],
        title='Isos Technology Python Cloud Automation Environment Test',
        subtitle=f'Atlassian Cloud Credentials\n\n\tThe current credentials are: \n\n\tURL: {p_auth_dict[url]}\n\tUsername: {p_auth_dict[username]}\n\tAPI Token: {p_auth_dict[api_token]}\n\n\t------------\n\n     This program will test access to: {p_auth_dict[remote_file]}\n\n\tWhat would you like to do?')

    if option == 0:
        jiraTest(p_auth_dict)
        accessTest(p_auth_dict)
    elif option == 1:
        updateParameters(param_pickle, p_auth_dict)
    else:
        exit(0)


def main():
    try:
        if imports:
            if not Path(param_pickle).exists():
                try:
                    Path(param_pickle).touch()
                    with open(param_pickle, 'wb') as pickled_parameters:
                        pickle.dump(auth_dict, pickled_parameters)
                except Exception as e:
                    print(
                        "There was an error trying to create your parameters cache: ", e, "\n\n")
                    exit(1)
            userParameters()
        else:
            exit(1)
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt, exiting...\n')
        exit(0)


if __name__ == '__main__':
    main()
