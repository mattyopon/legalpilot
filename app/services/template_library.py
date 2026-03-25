"""契約テンプレートライブラリサービス.

NDA/業務委託/売買/ライセンス等10種類の契約テンプレートを提供する。
"""

from __future__ import annotations

from app.knowledge.contract_templates import (
    get_all_template_types,
    get_template,
    get_template_text,
)
from app.models import ContractTemplate, ContractType


def _to_contract_type(type_str: str) -> ContractType:
    """文字列からContractTypeへ変換."""
    type_map = {ct.value: ct for ct in ContractType}
    return type_map.get(type_str, ContractType.NDA)


def get_contract_template(contract_type: str) -> ContractTemplate | None:
    """契約テンプレートを取得する.

    Args:
        contract_type: 契約種別文字列

    Returns:
        ContractTemplate or None
    """
    template = get_template(contract_type)
    if template is None:
        return None

    template_text = get_template_text(template)

    return ContractTemplate(
        contract_type=_to_contract_type(contract_type),
        name=template.name,
        description=template.description,
        template_text=template_text,
        key_points=list(template.key_points),
        warnings=list(template.warnings),
    )


def list_available_templates() -> list[dict[str, str]]:
    """利用可能なテンプレート一覧."""
    result = []
    for type_str in get_all_template_types():
        template = get_template(type_str)
        if template:
            result.append({
                "type": type_str,
                "name": template.name,
                "description": template.description,
            })
    return result


def search_templates(keyword: str) -> list[ContractTemplate]:
    """キーワードでテンプレートを検索."""
    results = []
    keyword_lower = keyword.lower()
    for type_str in get_all_template_types():
        template = get_template(type_str)
        if template is None:
            continue
        if (keyword_lower in template.name.lower()
                or keyword_lower in template.description.lower()
                or any(keyword_lower in s.lower() for s in template.sections)):
            ct = get_contract_template(type_str)
            if ct:
                results.append(ct)
    return results


def get_template_sections(contract_type: str) -> list[str]:
    """テンプレートの条項構成を取得."""
    template = get_template(contract_type)
    if template is None:
        return []
    return list(template.sections)
