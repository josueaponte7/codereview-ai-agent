from sqlalchemy import create_engine, text
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL.replace("postgresql://", "postgresql+psycopg://"))

def save_review(owner: str, repo: str, pr_number: int, pr_title: str, author: str, review: dict):
    query = text("""
        INSERT INTO reviews (
            owner, repo, pr_number, pr_title, author,
            arquitectura_score, arquitectura_observacion,
            naming_score, naming_observacion,
            solid_score, solid_observacion,
            deuda_tecnica_score, deuda_tecnica_observacion,
            seguridad_score, seguridad_observacion,
            veredicto
        ) VALUES (
            :owner, :repo, :pr_number, :pr_title, :author,
            :arquitectura_score, :arquitectura_observacion,
            :naming_score, :naming_observacion,
            :solid_score, :solid_observacion,
            :deuda_tecnica_score, :deuda_tecnica_observacion,
            :seguridad_score, :seguridad_observacion,
            :veredicto
        )
    """)

    with engine.connect() as conn:
        conn.execute(query, {
            "owner": owner,
            "repo": repo,
            "pr_number": pr_number,
            "pr_title": pr_title,
            "author": author,
            "arquitectura_score": review["arquitectura"]["score"],
            "arquitectura_observacion": review["arquitectura"]["observacion"],
            "naming_score": review["naming"]["score"],
            "naming_observacion": review["naming"]["observacion"],
            "solid_score": review["solid"]["score"],
            "solid_observacion": review["solid"]["observacion"],
            "deuda_tecnica_score": review["deuda_tecnica"]["score"],
            "deuda_tecnica_observacion": review["deuda_tecnica"]["observacion"],
            "seguridad_score": review["seguridad"]["score"],
            "seguridad_observacion": review["seguridad"]["observacion"],
            "veredicto": review["veredicto"]
        })
        conn.commit()

def get_reviews(owner: str, repo: str) -> list:
    query = text("""
        SELECT * FROM reviews
        WHERE owner = :owner AND repo = :repo
        ORDER BY created_at DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"owner": owner, "repo": repo})
        return [dict(row._mapping) for row in result]