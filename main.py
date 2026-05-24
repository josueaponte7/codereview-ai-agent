from core.github_client import get_pull_request, get_pull_request_diff

owner = "josueaponte7"
repo = "codereview-ai-agent"
pr_number = 1

pr = get_pull_request(owner, repo, pr_number)
print(f"PR: {pr['title']}")
print(f"Autor: {pr['user']['login']}")
print(f"Estado: {pr['state']}")