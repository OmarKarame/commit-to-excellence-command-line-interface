import click
from git import Repo
import git
import os
import requests

@click.group()
def cte():
    pass


def model_api_call(diff):
    # pass the diff into the model as a parameter and return the message
    url = 'https://cte-static-hctcd2f7fq-nw.a.run.app/predict'
    params = {
        'git_diff': diff
    }
    response = requests.get(url, params = params)
    result = response.json()
    return result['prediction']


# List of files that the user wants to commit
files = []



def find_git_directory():
    path = os.getcwd()
    while path != "/":
        if os.path.exists(os.path.join(path, '.git')):
            return path
        path = os.path.dirname(path)
    return None



def commit_empty_message():
    repo_path = find_git_directory()
    repo = git.Repo(f'{repo_path}')
    index = repo.index
    index.commit("")



def add_file_to_list(file):
    """Simple program that allows the user to add a file to commit"""
    files.append(file)


def connect_py():
    """Simple program that connects to repo to execute git commands"""
    repo_path = find_git_directory()
    repo = git.Repo(f'{repo_path}')
    # click.echo(f"Connected SUCCESSFULLY to: {repo}!")
    return repo


def get_last_commit_hash():
    repo = git.Repo('.')  # Initialize a Git repository object from the current directory
    head_commit = repo.head.commit  # Get the latest (HEAD) commit

    return head_commit.hexsha

def get_latest_commit_message():
    repo = git.Repo('.')  # Initialize a Git repository object from the current directory
    head_commit = repo.head.commit  # Get the latest (HEAD) commit

    click.echo(head_commit.message)   # Get the commit message











@cte.command()
def getcomm():
    repo = git.Repo('.')  # Initialize a Git repository object from the current directory
    head_commit = repo.head.commit  # Get the latest (HEAD) commit

    click.echo(head_commit.message)   # Get the commit message



@cte.command()
def connect():
    """Simple program that connects to repo to execute git commands"""
    repo_path = find_git_directory()
    repo = git.Repo(f'{repo_path}')
    click.echo(f"Connected SUCCESSFULLY to: {repo}!")
    return repo



@cte.command()
@click.option('-b','--branch', prompt='Checkout to branch',
              help='The branch you would like to change to/ work on')
def checkout(branch):
    """Simple program that allows user to checkout to another branch"""
    repo = connect_py()
    repo.git.checkout(branch)



@cte.command()
def status():
    """Simple program that prints git status"""
    repo = connect_py()
    click.echo(repo.git.status())



@cte.command()
@click.argument('file')
def add(file):
    """Simple program that allows the user to add a file to commit"""
    repo = connect_py()
    repo.git.add(os.path.abspath(file))



@cte.command()
@click.option('-m','--message', prompt='Add message to commit',
              help='The commit message you want to add to the staged file')
def commit(message):
    repo_path = find_git_directory()
    repo = git.Repo(f'{repo_path}')
    index = repo.index
    index.commit(message)



@cte.command()
def smartcommit():
    repo_path = find_git_directory()
    repo = git.Repo(f'{repo_path}')
    index = repo.index
    cached_diff = index.diff('HEAD')
    new_message = model_api_call(cached_diff)
    # {new_message}
    confirmation = click.confirm(f'''
                AI generated message:

                Added the word test to the end of the test.txt file


                Do you want to commit your file with this message?

                ''')
    if confirmation:
        # repo.git.commit('--amend' ,f'-m {new_message}')
        index.commit(f"{new_message}")
    else:
        new_message = click.prompt('Please type in your new message: ', type=str)
        # repo.git.commit('--amend' ,f'-m {new_message}')
        index.commit(f"{new_message}")


@cte.command()
@click.option('-r','--remote', default='origin', help='Name of the remote repository.')
@click.argument('branch')
def push(remote, branch):
    try:
        repo = git.Repo('.')

        repo.remotes[remote].fetch()

        repo.remotes[remote].push(branch)

        click.echo(f'Successfully pushed branch {branch} to {remote}.')
    except git.exc.GitCommandError as e:
        click.echo(f'Error: {e}')


@cte.command()
def get_diff():
    '''Simple program to get staged file info'''

    repo = connect_py()
    index = repo.index

    staged_files = [item.a_path for item in repo.index.diff(None)]

    diffs = repo.index.diff(None)

    for diff in diffs:
        print("File:", diff.a_path)
        print("Change Type:", diff.change_type)

        if diff.a_blob:
            print("Old Content:", diff.a_blob.data_stream.read())

        if diff.b_blob:
            print("New Content:", diff.b_blob.data_stream.read())

        print("Diff:\n", diff.diff)
        print("-" * 40)
