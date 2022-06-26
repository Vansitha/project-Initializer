from github import Github, GithubException
from decouple import config
import sys
import os

MAX_ARGS = 2
PROJECT_PATH = config("PROJECT_PATH")
TOKEN = config("ACCESS_TOKEN")
GITHUB = Github(TOKEN)
USER = GITHUB.get_user()


def get_folder_path(project_folder):
    """Generate the directory/folder path depending on the platform"""

    if os.name == "posix":
        return f"{PROJECT_PATH}/{project_folder}"
    return f"{PROJECT_PATH}\\{project_folder}"


def create_local_repo(project_folder):
    """Initializes a local git repo"""

    if os.path.isdir(project_folder):
        print(f"ERROR: folder named '{project_folder}' already exists in path")
        return False

    try:
        folder_path = get_folder_path(project_folder)
        os.mkdir(folder_path)
        os.chdir(folder_path)

        if os.name == "posix":
            os.system(f'touch README.md | echo "# {project_folder}" >> README.md')
        elif os.name == "nt":
            os.system(f'echo # {project_folder} > README.md')

        os.system("git init")
        os.system('git add README.md')
        os.system('git commit -m "initial commit"')
        print("Local Repository created successfully")
        return True
    
    except FileNotFoundError as fnfe:
        print("ERROR: project path is invalid")
        return False


def connect_to_remote(project_name):
    """Create repo on gitHub and connect with local repo"""

    try:
        USER.create_repo(project_name, private=True)
        username = USER.login
        git_url = f'https://github.com/{username}/{project_name}.git'
        os.system('git branch -M main')
        os.system(f'git remote add origin {git_url}')
        os.system('git push -u origin main')
        print("Connected to remote repository successfully")

    except GithubException as ge:
        print(ge.data["message"])


def main():

    project_name = None

    if (len(sys.argv) == MAX_ARGS):
        project_name = sys.argv[1]

    if (project_name != None):
        create_local_success = create_local_repo(project_name)
        if create_local_success:
            connect_to_remote(project_name)
    else:
        print("Usage: create <project-name>")


if __name__ == "__main__":
    main()