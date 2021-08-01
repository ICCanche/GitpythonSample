import os
from git import Repo
import time

local_repo_directory = os.path.join(os.getcwd(), 'GitpythonTuto')
destination = 'main'


def clone_repo():
    if os.path.exists(local_repo_directory):
        print("Directory exists, pulling changes from main branch")
        repo = Repo(local_repo_directory)
        origin = repo.remotes.origin
        origin.pull(destination)
    else:
        print("Directory does not exists, cloning")
        Repo.clone_from("git@github.com:ICCanche/GitpythonTuto.git",
                        local_repo_directory, branch=destination)


def chdirectory(path):
    os.chdir(path)

def create_branch(repo, branch_name):
    print("Creating a new branch with id name " + branch_name)
    current = repo.create_head(branch_name)
    current.checkout()

def update_file():
    print("Modifying the file")
    chdirectory(local_repo_directory)
    opened_file = open("file.txt", 'a')
    opened_file.write("{0} added at {1} \n".format(
        "I am a new string", str(time.time())))


def add_and_commit_changes(repo):
    print("Commiting changes")
    repo.git.add(update=True)
    repo.git.commit("-m", "Adding a new line to the file.text file")


def push_changes(repo, branch_name):
    print("Push changes")
    repo.git.push("--set-upstream", 'origin', branch_name)


def main():

    # clone the repository
    clone_repo()

    repo = Repo.init(local_repo_directory)
    branch_name = "feature/update-txt-file" + str(time.time())

    #create a new branch
    create_branch(repo, branch_name)

    # update file
    update_file()

    # add and commit changes
    add_and_commit_changes(repo)

    # push changes
    push_changes(repo, branch_name)


if __name__ == "__main__":
    main()
