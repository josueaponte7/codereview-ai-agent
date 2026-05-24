from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.github_client import get_pull_request, get_pull_request_diff
from core.repo_context import get_repo_files
from agent.reviewer import review_pull_request

router = APIRouter()

class ReviewRequest(BaseModel):
    owner: str
    repo: str
    pr_number: int

class ReviewResponse(BaseModel):
    pr_title: str
    author: str
    review: str

@router.post("/review", response_model=ReviewResponse)
async def review_pr(request: ReviewRequest):
    try:
        pr = get_pull_request(request.owner, request.repo, request.pr_number)
        diff = get_pull_request_diff(request.owner, request.repo, request.pr_number)
        files = get_repo_files(request.owner, request.repo)
        review = review_pull_request(pr['title'], diff, files)

        return ReviewResponse(
            pr_title=pr['title'],
            author=pr['user']['login'],
            review=review
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))