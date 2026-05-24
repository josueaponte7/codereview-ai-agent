def build_comment(review: dict, pr_title: str) -> str:
    score_emoji = lambda s: "🟢" if s >= 7 else "🟡" if s >= 4 else "🔴"
    veredicto_emoji = {
        "APROBADO": "✅",
        "CAMBIOS MENORES": "⚠️",
        "CAMBIOS MAYORES": "❌"
    }.get(review["veredicto"], "❓")

    total = sum([
        review["arquitectura"]["score"],
        review["naming"]["score"],
        review["solid"]["score"],
        review["deuda_tecnica"]["score"],
        review["seguridad"]["score"]
    ])
    promedio = round(total / 5, 1)

    return f"""## 🤖 CodeReview AI Agent

**{veredicto_emoji} Veredicto: {review["veredicto"]}** | Score global: **{promedio}/10**

| Categoría | Score | Observación |
|-----------|-------|-------------|
| Arquitectura | {score_emoji(review["arquitectura"]["score"])} {review["arquitectura"]["score"]}/10 | {review["arquitectura"]["observacion"]} |
| Naming | {score_emoji(review["naming"]["score"])} {review["naming"]["score"]}/10 | {review["naming"]["observacion"]} |
| SOLID | {score_emoji(review["solid"]["score"])} {review["solid"]["score"]}/10 | {review["solid"]["observacion"]} |
| Deuda Técnica | {score_emoji(review["deuda_tecnica"]["score"])} {review["deuda_tecnica"]["score"]}/10 | {review["deuda_tecnica"]["observacion"]} |
| Seguridad | {score_emoji(review["seguridad"]["score"])} {review["seguridad"]["score"]}/10 | {review["seguridad"]["observacion"]} |

---
*Revisado automáticamente por [CodeReview AI Agent](https://github.com/josueaponte7/codereview-ai-agent)*
"""