import os
import requests
import datetime

owner = "python"
repo = "cpython"
token = os.getenv("GITHUB_TOKEN")

print(token)

thirty_days_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).isoformat()

commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
params = {
    "since": thirty_days_ago,
    "per_page": 100 
}
headers = {
    "Authorization": f"token {token}"
}
response = requests.get(commits_url, params=params, headers=headers)
commits = response.json()

origin_owner = "savannahostrowski"
origin_repo= "jit_stencils"
origin_workflow_id = "generate_stencils.yml"
for commit in commits:
    sha = commit["sha"]
    message = commit["commit"]["message"]
    print(f"Triggering workflow for commit {sha}: {message}")

    dispatch_url = f"https://api.github.com/repos/{origin_owner}/{origin_repo}/actions/workflows/{origin_workflow_id}/dispatches"
    data = {
        "ref": "main", 
        "inputs": {
            "commit_sha": sha
        }
    }
    response = requests.post(dispatch_url, json=data, headers=headers)
    if response.status_code == 204:
        print(f"Successfully triggered workflow for commit {sha}")
    else:
        print(f"Failed to trigger workflow for commit {sha}: {response.text}")