from setuptools import setup, find_packages

setup(
    name='commit-to-excellence',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'gitpython'
    ],
    entry_points=''''
        [console_scripts]
        cte=commit_to_excellence:cte
    '''
)


# Run these on terminal:
# pip install --editable .
