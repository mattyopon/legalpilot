"""契約書レビューAIサービス.

契約テキスト入力からリスク条項を検出し、修正提案を行う。
"""

from __future__ import annotations

from app.knowledge.contract_risks import CONTRACT_RISK_PATTERNS, RiskPattern
from app.models import ContractReviewResult, RiskClause, RiskLevel


def _detect_risk_clause(text: str, pattern: RiskPattern) -> RiskClause | None:
    """テキストからリスク条項を検出."""
    text_lower = text.lower()
    matched_keywords = [kw for kw in pattern.keywords if kw.lower() in text_lower]
    if not matched_keywords:
        return None

    # キーワードを含む周辺テキストを抽出
    first_kw = matched_keywords[0].lower()
    idx = text_lower.find(first_kw)
    start = max(0, idx - 50)
    end = min(len(text), idx + len(first_kw) + 100)
    clause_text = text[start:end].strip()

    return RiskClause(
        clause_text=clause_text,
        risk_type=pattern.risk_type,
        risk_level=RiskLevel(pattern.risk_level),
        description=pattern.description,
        suggestion=pattern.suggestion,
        legal_basis=pattern.legal_basis,
    )


def _determine_overall_risk(risk_clauses: list[RiskClause]) -> RiskLevel:
    """全体のリスクレベルを判定."""
    if not risk_clauses:
        return RiskLevel.INFO
    if any(r.risk_level == RiskLevel.CRITICAL for r in risk_clauses):
        return RiskLevel.CRITICAL
    if any(r.risk_level == RiskLevel.HIGH for r in risk_clauses):
        return RiskLevel.HIGH
    if any(r.risk_level == RiskLevel.MEDIUM for r in risk_clauses):
        return RiskLevel.MEDIUM
    if any(r.risk_level == RiskLevel.LOW for r in risk_clauses):
        return RiskLevel.LOW
    return RiskLevel.INFO


def review_contract(contract_text: str) -> ContractReviewResult:
    """契約書をレビューしてリスク条項を検出する.

    Args:
        contract_text: 契約書テキスト

    Returns:
        ContractReviewResult
    """
    if not contract_text.strip():
        return ContractReviewResult(
            contract_text=contract_text,
            risk_clauses=[],
            overall_risk=RiskLevel.INFO,
            summary="契約書テキストが空です。",
        )

    risk_clauses: list[RiskClause] = []
    for pattern in CONTRACT_RISK_PATTERNS:
        clause = _detect_risk_clause(contract_text, pattern)
        if clause:
            risk_clauses.append(clause)

    # リスクレベルでソート
    risk_order = {RiskLevel.CRITICAL: 0, RiskLevel.HIGH: 1, RiskLevel.MEDIUM: 2, RiskLevel.LOW: 3, RiskLevel.INFO: 4}
    risk_clauses.sort(key=lambda r: risk_order.get(r.risk_level, 5))

    overall_risk = _determine_overall_risk(risk_clauses)

    critical_count = sum(1 for r in risk_clauses if r.risk_level == RiskLevel.CRITICAL)
    high_count = sum(1 for r in risk_clauses if r.risk_level == RiskLevel.HIGH)

    recommendations: list[str] = []
    if critical_count > 0:
        recommendations.append(f"CRITICAL リスクが{critical_count}件あります。契約締結前に必ず修正してください。")
    if high_count > 0:
        recommendations.append(f"HIGH リスクが{high_count}件あります。修正を強く推奨します。")
    if not risk_clauses:
        recommendations.append("明らかなリスク条項は検出されませんでした。ただし、専門家による最終確認を推奨します。")

    summary = (
        f"契約書レビュー完了: {len(risk_clauses)}件のリスク条項を検出"
        f"（CRITICAL: {critical_count}件, HIGH: {high_count}件）"
        f" 総合リスク: {overall_risk.value.upper()}"
    )

    return ContractReviewResult(
        contract_text=contract_text,
        risk_clauses=risk_clauses,
        overall_risk=overall_risk,
        summary=summary,
        recommendations=recommendations,
    )


def get_risk_summary_by_type(result: ContractReviewResult) -> dict[str, int]:
    """リスクタイプ別のサマリー."""
    summary: dict[str, int] = {}
    for clause in result.risk_clauses:
        summary[clause.risk_type] = summary.get(clause.risk_type, 0) + 1
    return summary
