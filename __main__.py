import os
import aiohttp
from git import Repo
import time
from decouple import config
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
import asyncio

user_name = config('USER_NAME')
repository = config('REPOSITORY')

local_repo_directory = os.path.join(os.getcwd(), repository)
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


async def setup_github(branch_name):
    print("Setup github token")
    api_token = config('GH_API_TOKEN')

    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, user_name, oauth_token=api_token)
        
        #create-pull-request
        await create_pull_request(gh, branch_name, api_token)

async def create_pull_request(gh, branch_name, token):
    print("Creating PR from: " + branch_name)
    response = await gh.post('/repos/{owner}/{repo}/pulls', url_vars={'owner': user_name, 'repo': repository}, data = {
        'title': 'Addition of a new line to the file.txt',
        'head': branch_name,
        'body': '\n #What does this PR do? \n Add a new text line to the main text file',
        'base': destination
    }, accept='application/vnd.github.v3+json', oauth_token=token)
    if response:
        print("PR was created at: " + response['html_url'])


async def main():
    #clone the repository
    clone_repo()

    repo = Repo.init(local_repo_directory)
    branch_name = "feature/update-txt-file" + str(time.time())
    gh_token = config('GH_API_TOKEN')

    #create a new branch
    create_branch(repo, branch_name)

    # update file
    update_file()

    # add and commit changes
    add_and_commit_changes(repo)

    # push changes
    push_changes(repo, branch_name)

    #setup github credentials and session
    await setup_github(branch_name)

if __name__ == "__main__":
    #Only for windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #run main async
    asyncio.run(main())
