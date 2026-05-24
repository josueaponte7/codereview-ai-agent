from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.github_client import get_pull_request, get_pull_request_diff
from core.repo_context import get_repo_files
from core.database import save_review, get_reviews
from agent.reviewer import review_pull_request
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

class ReviewRequest(BaseModel):
    owner: str
    repo: str
    pr_number: int

class CategoryScore(BaseModel):
    score: int
    observacion: str

class ReviewResponse(BaseModel):
    pr_title: str
    author: str
    arquitectura: CategoryScore
    naming: CategoryScore
    solid: CategoryScore
    deuda_tecnica: CategoryScore
    seguridad: CategoryScore
    veredicto: str

@router.post("/review", response_model=ReviewResponse)
async def review_pr(request: ReviewRequest):
    try:
        pr = get_pull_request(request.owner, request.repo, request.pr_number)
        diff = get_pull_request_diff(request.owner, request.repo, request.pr_number)
        files = get_repo_files(request.owner, request.repo)
        review = review_pull_request(pr['title'], diff, files)

        save_review(
            owner=request.owner,
            repo=request.repo,
            pr_number=request.pr_number,
            pr_title=pr['title'],
            author=pr['user']['login'],
            review=review
        )

        return ReviewResponse(
            pr_title=pr['title'],
            author=pr['user']['login'],
            **review
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reviews/{owner}/{repo}")
async def list_reviews(owner: str, repo: str):
    try:
        return get_reviews(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    # GitHub envía un ping al crear el webhook — ignorarlo correctamente
    event = request.headers.get("X-Github-Event", "")
    if event == "ping":
        return {"status": "pong"}

    action = payload.get("action")
    if action not in ["opened", "reopened", "synchronize"]:
        return {"status": "ignored"}

    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})

    owner = repo["owner"]["login"]
    repo_name = repo["name"]
    pr_number = pr["number"]
    pr_title = pr["title"]
    author = pr["user"]["login"]

    diff = get_pull_request_diff(owner, repo_name, pr_number)
    files = get_repo_files(owner, repo_name)
    review = review_pull_request(pr_title, diff, files)

    save_review(
        owner=owner,
        repo=repo_name,
        pr_number=pr_number,
        pr_title=pr_title,
        author=author,
        review=review
    )

    return {"status": "reviewed", "veredicto": review["veredicto"]}