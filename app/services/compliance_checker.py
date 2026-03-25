"""コンプライアンスチェックサービス.

業種別の法令遵守チェックリストを生成し、適合状況を評価する。
"""

from __future__ import annotations

from dataclasses import dataclass

from app.knowledge.japan_laws import get_laws_for_industry
from app.models import (
    ComplianceCheckItem,
    ComplianceCheckResult,
    IndustryType,
    RiskLevel,
)


@dataclass
class ComplianceInput:
    """コンプライアンスチェック入力."""
    industry: IndustryType
    has_privacy_policy: bool = False
    has_terms_of_service: bool = False
    has_proper_contracts: bool = False
    has_subcontract_compliance: bool = False
    has_anti_monopoly_compliance: bool = False
    has_consumer_protection: bool = False
    has_ip_management: bool = False
    has_data_security: bool = False
    has_employee_handbook: bool = False
    has_whistleblower_system: bool = False




def _check_law_compliance(
    law_id: str,
    law_name: str,
    category: str,
    key_requirements: list[str],
    compliance_flags: dict[str, bool],
) -> list[ComplianceCheckItem]:
    """法令ごとのコンプライアンスチェック."""
    items: list[ComplianceCheckItem] = []

    flag_map: dict[str, list[str]] = {
        "has_privacy_policy": ["CL05"],
        "has_terms_of_service": ["CL06", "CL07", "CL10"],
        "has_proper_contracts": ["CL01", "CL02", "CL03"],
        "has_subcontract_compliance": ["CL04"],
        "has_anti_monopoly_compliance": ["CL09"],
        "has_consumer_protection": ["CL06", "CL07"],
        "has_ip_management": ["CL08"],
        "has_data_security": ["CL05", "CL11"],
        "has_employee_handbook": ["CL14", "CL15"],
        "has_whistleblower_system": ["CL09"],
    }

    is_compliant = False
    for flag_name, applicable_laws in flag_map.items():
        if law_id in applicable_laws and compliance_flags.get(flag_name, False):
            is_compliant = True
            break

    if is_compliant:
        risk_level = RiskLevel.INFO
        recommendation = "適合確認済み。定期的な見直しを推奨します。"
    else:
        if category in ("契約", "債権", "商取引"):
            risk_level = RiskLevel.MEDIUM
        elif category in ("個人情報", "消費者保護", "労働"):
            risk_level = RiskLevel.HIGH
        elif category in ("下請",):
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.MEDIUM
        recommendation = f"{law_name}の要件を確認し、必要な対応を実施してください。"

    items.append(ComplianceCheckItem(
        category=category,
        item_name=law_name,
        description=f"主要要件: {', '.join(key_requirements[:3])}",
        is_compliant=is_compliant,
        risk_level=risk_level,
        recommendation=recommendation,
        legal_basis=law_name,
    ))

    return items


def check_compliance(input_data: ComplianceInput) -> ComplianceCheckResult:
    """業種別コンプライアンスチェックを実行.

    Args:
        input_data: コンプライアンスチェック入力

    Returns:
        ComplianceCheckResult
    """
    laws = get_laws_for_industry(input_data.industry.value)

    compliance_flags = {
        "has_privacy_policy": input_data.has_privacy_policy,
        "has_terms_of_service": input_data.has_terms_of_service,
        "has_proper_contracts": input_data.has_proper_contracts,
        "has_subcontract_compliance": input_data.has_subcontract_compliance,
        "has_anti_monopoly_compliance": input_data.has_anti_monopoly_compliance,
        "has_consumer_protection": input_data.has_consumer_protection,
        "has_ip_management": input_data.has_ip_management,
        "has_data_security": input_data.has_data_security,
        "has_employee_handbook": input_data.has_employee_handbook,
        "has_whistleblower_system": input_data.has_whistleblower_system,
    }

    all_items: list[ComplianceCheckItem] = []
    for law in laws:
        items = _check_law_compliance(
            law.law_id, law.law_name, law.category,
            law.key_requirements, compliance_flags,
        )
        all_items.extend(items)

    total = len(all_items)
    compliant = sum(1 for i in all_items if i.is_compliant)
    score = (compliant / total * 100) if total > 0 else 0.0

    non_compliant = total - compliant
    summary = (
        f"コンプライアンスチェック完了 ({input_data.industry.value}): "
        f"{total}項目中{compliant}項目が適合。スコア: {score:.1f}/100。"
        f"要対応: {non_compliant}項目"
    )

    return ComplianceCheckResult(
        industry=input_data.industry,
        items=all_items,
        score=score,
        summary=summary,
    )


def get_supported_industries() -> list[str]:
    """サポート対象の業種一覧."""
    return [i.value for i in IndustryType]
