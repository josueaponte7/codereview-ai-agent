import requests
import base64
from core.config import GITHUB_TOKEN

BASE_URL = "https://api.github.com"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repo_files(owner: str, repo: str) -> list[str]:
    url = f"{BASE_URL}/repos/{owner}/{repo}/git/trees/main?recursive=1"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    tree = response.json().get("tree", [])
    return [item["path"] for item in tree if item["type"] == "blob"]

def get_file_content(owner: str, repo: str, path: str) -> str:
    url = f"{BASE_URL}/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content = response.json().get("content", "")
    return base64.b64decode(content).decode("utf-8", errors="ignore")