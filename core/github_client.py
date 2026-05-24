import requests
from core.config import GITHUB_TOKEN

BASE_URL = "https://api.github.com"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_pull_request(owner: str, repo: str, pr_number: int) -> dict:
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_pull_request_diff(owner: str, repo: str, pr_number: int) -> str:
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    diff_headers = {**headers, "Accept": "application/vnd.github.v3.diff"}
    response = requests.get(url, headers=diff_headers)
    response.raise_for_status()
    return response.text