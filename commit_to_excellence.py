import click
from git import Repo
import git
import os

@click.group()
def cte():
    click.echo("")


def model_api_call():
    return "This is your commit message :)"


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
def aicommit():
    repo_path = find_git_directory()
    repo = git.Repo(f'{repo_path}')
    index = repo.index
    index.commit("")
    commit_hash = get_last_commit_hash()
    commit = repo.commit(commit_hash)
    new_message = model_api_call()
    confirmation = click.confirm(f'''
                 AI generated message:

                 {new_message}

                 Do you want to commit your file with this message?

                 ''')
    if confirmation:
        repo.git.commit(
            '--amend', '-C', commit_hash, author=commit.author
        )
    else:
        click.prompt('Please type int your new message: ', type=str)




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
