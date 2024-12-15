import os
import requests
import datetime

# GitHub repository details
owner = "python"
repo = "cpython"
workflow_id = "generate_stencils.yml"  # The name of your workflow file
token = os.getenv("GITHUB_TOKEN")  # Personal access token with repo scope

print(token)

# Calculate the date 30 days ago
thirty_days_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).isoformat()

# Fetch commits from the last 30 days
commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
params = {
    "since": thirty_days_ago,
    "per_page": 100  # Adjust as needed
}
headers = {
    "Authorization": f"token {token}"
}
response = requests.get(commits_url, params=params, headers=headers)
commits = response.json()

origin_owner = "savannahostrowski"
origin_repo= "jit_stencils"
origin_workflow_id = "generate_stencils.yml"
# Trigger the workflow for each commit
for commit in commits:
    sha = commit["sha"]
    message = commit["commit"]["message"]
    print(f"Triggering workflow for commit {sha}: {message}")

    # Trigger the workflow_dispatch event
    dispatch_url = f"https://api.github.com/repos/{origin_owner}/{origin_repo}/actions/workflows/{origin_workflow_id}/dispatches"
    data = {
        "ref": "main",  # The branch to run the workflow on
        "inputs": {
            "commit_sha": sha,
            "commit_message": message
        }
    }
    response = requests.post(dispatch_url, json=data, headers=headers)
    if response.status_code == 204:
        print(f"Successfully triggered workflow for commit {sha}")
    else:
        print(f"Failed to trigger workflow for commit {sha}: {response.text}")