
import os
import github

# extracting all the input from environments
token = os.environ['GITHUB_TOKEN']

github = github.Github(token)
# GITHUB_REPOSITORY is the repo name in owner/name format in Github Workflow
repo = github.get_repo(os.environ['GITHUB_REPOSITORY'])
print(os.environ.get("GITHUB_EVENT_PATH"))
