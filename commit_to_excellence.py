import click
from git import Repo
import git
import os

@click.group()
def cte():
    click.echo("")

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
    # for item in repo.index.diff(None):
    #     click.echo(f'File {item.a_path} committed!')


def add_file_to_list(file):
    """Simple program that allows the user to add a file to commit"""
    files.append(file)



# https://github.com/OmarKarame/Commit-To-Excellence-Backend
# OmarKarame/Commit-To-Excellence-Backend
# /Users/omarkarame/code/OmarKarame/Commit-To-Excellence/Commit-To-Excellence-Backend
# Code-Test-click-application-with-python-methods#34


def connect_py():
    """Simple program that connects to repo to execute git commands"""
    repo_path = find_git_directory()
    repo = git.Repo(f'{repo_path}')
    # click.echo(f"Connected SUCCESSFULLY to: {repo}!")
    return repo


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
    click.echo(f"Success!")


@cte.command()
@click.option('-r','--remote', default='origin', help='Name of the remote repository.')
@click.argument('branch')
def push(remote, branch):
    """
    Push code to a GitHub repository.
    """
    try:
        repo = git.Repo('.')  # Initialize a Git repository object from the current directory

        # Fetch the remote repository to ensure you have the latest changes
        repo.remotes[remote].fetch()

        # Push the specified branch to the remote repository
        repo.remotes[remote].push(branch)

        click.echo(f'Successfully pushed branch {branch} to {remote}.')
    except git.exc.GitCommandError as e:
        click.echo(f'Error: {e}')


@cte.command()
def get_diff():
    """Simple program that allows the user to get info about staged files"""
    repo = connect_py()
    index = repo.index
    # Get staged (added) files
    staged_files = [item.a_path for item in repo.index.diff(None)]

    diffs = repo.index.diff(None)

    for diff in diffs:
        print("File:", diff.a_path)
        print("Change Type:", diff.change_type)

        if diff.a_blob:  # Check if a_blob is not None
            print("Old Content:", diff.a_blob.data_stream.read())

        if diff.b_blob:  # Check if b_blob is not None
            print("New Content:", diff.b_blob.data_stream.read())

        print("Diff:\n", diff.diff)
        print("-" * 40)


# if __name__ == '__main__':
#     get_diff()
