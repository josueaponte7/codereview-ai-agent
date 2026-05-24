from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from agent.prompts.review_prompt import REVIEW_SYSTEM_PROMPT, build_review_prompt
from core.config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

def review_pull_request(pr_title: str, diff: str) -> str:
    messages = [
        SystemMessage(content=REVIEW_SYSTEM_PROMPT),
        HumanMessage(content=build_review_prompt(diff, pr_title))
    ]
    response = llm.invoke(messages)
    return response.content