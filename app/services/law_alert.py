"""法改正アラートサービス.

業種に影響する法改正の検知とインパクト分析を行う。
"""

from __future__ import annotations

from app.models import IndustryType, LawAlert, RiskLevel


# 法改正アラートのデータベース（実際にはAPI連携や定期更新を想定）
LAW_ALERTS: list[LawAlert] = [
    LawAlert(
        law_name="個人情報保護法改正",
        alert_type="法改正",
        description="個人情報保護法の改正に伴い、個人データの越境移転に関する規制が強化されます。",
        impact_level=RiskLevel.HIGH,
        affected_industries=[IndustryType.IT, IndustryType.FINANCE, IndustryType.HEALTHCARE, IndustryType.RETAIL],
        effective_date="2025-04-01",
        action_items=["プライバシーポリシーの改定", "越境移転に関する同意取得プロセスの見直し", "個人情報管理体制の再点検"],
        source="個人情報保護委員会",
    ),
    LawAlert(
        law_name="下請法運用基準改正",
        alert_type="運用基準変更",
        description="下請法の運用基準が改正され、買いたたきの判断基準が厳格化されます。",
        impact_level=RiskLevel.HIGH,
        affected_industries=[IndustryType.IT, IndustryType.MANUFACTURING],
        effective_date="2025-01-01",
        action_items=["下請取引の見直し", "発注書面の再点検", "下請事業者との取引条件の確認"],
        source="公正取引委員会",
    ),
    LawAlert(
        law_name="フリーランス保護新法",
        alert_type="新法施行",
        description="フリーランス・事業者間取引適正化等法が施行され、業務委託に関する書面交付義務等が導入されます。",
        impact_level=RiskLevel.HIGH,
        affected_industries=[IndustryType.IT, IndustryType.OTHER],
        effective_date="2024-11-01",
        action_items=["業務委託契約書の見直し", "取引条件の書面明示", "フリーランスへの60日以内の支払い確保"],
        source="厚生労働省・公正取引委員会",
    ),
    LawAlert(
        law_name="電子帳簿保存法改正",
        alert_type="法改正",
        description="電子取引データの電子保存義務化の完全施行。紙での保存が認められなくなります。",
        impact_level=RiskLevel.MEDIUM,
        affected_industries=[IndustryType.IT, IndustryType.FINANCE, IndustryType.RETAIL, IndustryType.MANUFACTURING, IndustryType.OTHER],
        effective_date="2024-01-01",
        action_items=["電子取引データの保存システム導入", "検索要件を満たす保存体制の構築", "社内規程の整備"],
        source="国税庁",
    ),
    LawAlert(
        law_name="景品表示法改正",
        alert_type="法改正",
        description="確約手続の導入やステルスマーケティングの規制強化が行われます。",
        impact_level=RiskLevel.MEDIUM,
        affected_industries=[IndustryType.RETAIL, IndustryType.IT, IndustryType.FOOD],
        effective_date="2024-10-01",
        action_items=["広告表示の再点検", "インフルエンサーマーケティングの表示確認", "PR表記ガイドラインの策定"],
        source="消費者庁",
    ),
    LawAlert(
        law_name="不正競争防止法改正",
        alert_type="法改正",
        description="デジタル空間での営業秘密保護が強化され、メタバース上の模倣品対策等が盛り込まれます。",
        impact_level=RiskLevel.LOW,
        affected_industries=[IndustryType.IT, IndustryType.MANUFACTURING],
        effective_date="2024-04-01",
        action_items=["営業秘密管理体制の確認", "デジタルコンテンツの権利保護施策の見直し"],
        source="経済産業省",
    ),
    LawAlert(
        law_name="医療DX推進関連法",
        alert_type="新法施行",
        description="電子処方箋・オンライン診療に関する規制緩和と情報セキュリティ要件の強化。",
        impact_level=RiskLevel.HIGH,
        affected_industries=[IndustryType.HEALTHCARE],
        effective_date="2025-04-01",
        action_items=["電子処方箋対応システムの導入", "情報セキュリティポリシーの改定", "患者同意取得プロセスの見直し"],
        source="厚生労働省",
    ),
    LawAlert(
        law_name="金融商品取引法改正",
        alert_type="法改正",
        description="暗号資産・ステーブルコインに関する規制の整備。AML/CFT対応の強化。",
        impact_level=RiskLevel.HIGH,
        affected_industries=[IndustryType.FINANCE],
        effective_date="2025-06-01",
        action_items=["暗号資産取扱いに関する社内規程の整備", "AML/CFT体制の強化", "顧客管理の厳格化"],
        source="金融庁",
    ),
    LawAlert(
        law_name="食品表示法改正",
        alert_type="法改正",
        description="アレルギー表示の義務化範囲拡大と原料原産地表示の厳格化。",
        impact_level=RiskLevel.MEDIUM,
        affected_industries=[IndustryType.FOOD, IndustryType.RETAIL],
        effective_date="2025-04-01",
        action_items=["食品表示ラベルの再確認", "原料調達先の原産地情報の整備", "アレルギー表示の更新"],
        source="消費者庁",
    ),
    LawAlert(
        law_name="建設業法改正",
        alert_type="法改正",
        description="建設業の担い手確保に向けた施工体制の適正化と処遇改善。",
        impact_level=RiskLevel.MEDIUM,
        affected_industries=[IndustryType.MANUFACTURING],
        effective_date="2025-04-01",
        action_items=["施工体制の見直し", "下請事業者の処遇改善", "技能者の処遇改善"],
        source="国土交通省",
    ),
]


def get_alerts_for_industry(industry: IndustryType) -> list[LawAlert]:
    """業種に関連する法改正アラートを取得.

    Args:
        industry: 業種

    Returns:
        関連するアラートのリスト（影響度順）
    """
    relevant = [a for a in LAW_ALERTS if industry in a.affected_industries]
    risk_order = {RiskLevel.CRITICAL: 0, RiskLevel.HIGH: 1, RiskLevel.MEDIUM: 2, RiskLevel.LOW: 3, RiskLevel.INFO: 4}
    relevant.sort(key=lambda a: risk_order.get(a.impact_level, 5))
    return relevant


def get_all_alerts() -> list[LawAlert]:
    """全アラートを取得."""
    return list(LAW_ALERTS)


def get_alerts_by_impact(min_level: RiskLevel) -> list[LawAlert]:
    """指定レベル以上の影響度のアラートを取得."""
    risk_order = {RiskLevel.CRITICAL: 0, RiskLevel.HIGH: 1, RiskLevel.MEDIUM: 2, RiskLevel.LOW: 3, RiskLevel.INFO: 4}
    min_order = risk_order.get(min_level, 5)
    return [a for a in LAW_ALERTS if risk_order.get(a.impact_level, 5) <= min_order]


def get_alert_summary(industry: IndustryType) -> dict[str, int]:
    """業種別のアラートサマリー."""
    alerts = get_alerts_for_industry(industry)
    summary: dict[str, int] = {}
    for a in alerts:
        level = a.impact_level.value
        summary[level] = summary.get(level, 0) + 1
    return summary
