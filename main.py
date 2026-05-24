from core.github_client import get_pull_request, get_pull_request_diff
from agent.reviewer import review_pull_request

owner = "josueaponte7"
repo = "codereview-ai-agent"
pr_number = 1

pr = get_pull_request(owner, repo, pr_number)
diff = get_pull_request_diff(owner, repo, pr_number)

print(f"Revisando PR: {pr['title']}\n")

review = review_pull_request(pr['title'], diff)
print(review)