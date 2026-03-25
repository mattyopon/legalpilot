"""契約テンプレート構造のナレッジベース."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TemplateStructure:
    template_id: str
    contract_type: str
    name: str
    description: str
    sections: list[str]
    key_points: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


CONTRACT_TEMPLATES: dict[str, TemplateStructure] = {
    "nda": TemplateStructure(
        template_id="T01", contract_type="nda", name="秘密保持契約書（NDA）",
        description="相互または一方の秘密情報の開示・保護に関する契約",
        sections=["契約当事者", "秘密情報の定義", "秘密保持義務", "例外事項", "目的外使用の禁止", "秘密情報の返還・廃棄", "有効期間", "損害賠償", "管轄裁判所"],
        key_points=["秘密情報の範囲を明確に定義する", "例外事項（公知情報等）を設ける", "秘密保持期間を合理的に設定する（通常3-5年）", "損害賠償条項を設ける"],
        warnings=["秘密情報の範囲が広すぎると実務上運用困難", "無期限の秘密保持義務は避ける"],
    ),
    "service_agreement": TemplateStructure(
        template_id="T02", contract_type="service_agreement", name="業務委託契約書",
        description="業務の委託・受託に関する契約",
        sections=["契約当事者", "委託業務の内容", "業務遂行方法", "納期・検収", "報酬・支払条件", "秘密保持", "知的財産権", "損害賠償", "契約解除", "反社排除", "管轄裁判所"],
        key_points=["業務内容を具体的に記載する", "検収基準を明確にする", "支払条件（下請法の場合60日以内）を遵守する", "成果物の権利帰属を明確にする"],
        warnings=["下請法適用の有無を確認する", "偽装請負にならないよう指揮命令関係に注意"],
    ),
    "sales": TemplateStructure(
        template_id="T03", contract_type="sales", name="売買契約書",
        description="物品の売買に関する契約",
        sections=["契約当事者", "目的物", "数量", "代金", "支払条件", "引渡条件", "検収", "契約不適合責任", "危険負担", "所有権移転", "損害賠償", "管轄裁判所"],
        key_points=["目的物の仕様を明確にする", "検収基準と期間を定める", "契約不適合責任の期間を設定する", "危険負担と所有権移転時期を明確にする"],
        warnings=["継続的売買の場合は基本契約と個別契約を分ける"],
    ),
    "license": TemplateStructure(
        template_id="T04", contract_type="license", name="ライセンス契約書",
        description="知的財産権の使用許諾に関する契約",
        sections=["契約当事者", "ライセンスの対象", "許諾範囲", "ロイヤリティ", "使用条件", "禁止事項", "保証・免責", "契約期間", "解除条件", "管轄裁判所"],
        key_points=["許諾範囲（独占/非独占、地域、期間）を明確にする", "サブライセンスの可否を定める", "ロイヤリティの計算方法を明記する"],
        warnings=["独占的ライセンスの場合は競業避止との関係に注意"],
    ),
    "employment": TemplateStructure(
        template_id="T05", contract_type="employment", name="雇用契約書",
        description="労働者の雇用に関する契約",
        sections=["契約当事者", "業務内容", "就業場所", "労働時間", "休日・休暇", "賃金", "退職に関する事項", "社会保険", "秘密保持", "競業避止"],
        key_points=["労働条件を書面で明示する（労基法第15条）", "試用期間を設ける場合は明記する", "固定残業代がある場合は時間数と金額を明記する"],
        warnings=["労基法の最低基準を下回る条件は無効", "有期雇用の場合は更新基準を明示する"],
    ),
    "lease": TemplateStructure(
        template_id="T06", contract_type="lease", name="賃貸借契約書",
        description="不動産・動産の賃貸借に関する契約",
        sections=["契約当事者", "目的物", "使用目的", "賃料・管理費", "敷金・保証金", "契約期間", "修繕義務", "原状回復", "解約条件", "禁止事項"],
        key_points=["賃料改定条件を明記する", "原状回復の範囲を具体的に定める", "敷金の返還条件を明確にする"],
        warnings=["消費者契約法により不当な条項は無効となる可能性がある"],
    ),
    "consulting": TemplateStructure(
        template_id="T07", contract_type="consulting", name="コンサルティング契約書",
        description="コンサルティング業務の委託に関する契約",
        sections=["契約当事者", "業務範囲", "成果物", "報酬・費用", "秘密保持", "知的財産権", "競業避止", "免責事項", "契約期間", "管轄裁判所"],
        key_points=["業務範囲を明確にし、追加業務の扱いを定める", "成果物の定義と帰属を明記する", "報酬体系（時間制/プロジェクト制/成功報酬）を明確にする"],
        warnings=["助言の成果保証は避ける", "利益相反の確認を行う"],
    ),
    "subcontracting": TemplateStructure(
        template_id="T08", contract_type="subcontracting", name="下請契約書",
        description="下請法に基づく製造委託・役務委託の契約",
        sections=["契約当事者", "委託内容", "下請代金", "支払期日", "検収方法", "不良品の取扱い", "知的財産権", "秘密保持", "下請法遵守事項"],
        key_points=["発注書面の3条書面を交付する", "支払期日を受領日から60日以内に設定する", "減額・返品の禁止を確認する"],
        warnings=["下請法違反は公正取引委員会の勧告対象となる"],
    ),
    "joint_venture": TemplateStructure(
        template_id="T09", contract_type="joint_venture", name="合弁事業契約書",
        description="複数当事者による共同事業に関する契約",
        sections=["契約当事者", "事業目的", "出資比率", "役員構成", "意思決定方法", "利益配分", "追加出資", "株式譲渡制限", "デッドロック解消", "撤退条件"],
        key_points=["意思決定プロセスを明確にする", "デッドロック解消メカニズムを設ける", "撤退時の手続きと条件を定める"],
        warnings=["独占禁止法の企業結合規制に注意", "少数株主の権利保護を考慮する"],
    ),
    "franchise": TemplateStructure(
        template_id="T10", contract_type="franchise", name="フランチャイズ契約書",
        description="フランチャイズ事業に関する契約",
        sections=["契約当事者", "事業内容", "テリトリー", "加盟金・ロイヤリティ", "商標使用", "オペレーションマニュアル", "研修", "品質管理", "契約期間", "契約終了後の義務"],
        key_points=["開示書面（法定開示事項）を事前に提供する", "ロイヤリティの計算方法を明記する", "テリトリー権の範囲を明確にする"],
        warnings=["中小小売商業振興法の開示義務を遵守する", "独占禁止法の優越的地位の濫用に注意"],
    ),
}


def get_template(contract_type: str) -> TemplateStructure | None:
    return CONTRACT_TEMPLATES.get(contract_type)


def get_all_template_types() -> list[str]:
    return list(CONTRACT_TEMPLATES.keys())


def get_template_text(template: TemplateStructure) -> str:
    """テンプレートからテキストを生成."""
    lines = [f"# {template.name}", "", f"{template.description}", "", "## 条項構成", ""]
    for i, section in enumerate(template.sections, 1):
        lines.append(f"第{i}条（{section}）")
        lines.append(f"  {section}に関する事項を定める。")
        lines.append("")
    lines.append("## 留意事項")
    for kp in template.key_points:
        lines.append(f"- {kp}")
    lines.append("")
    lines.append("## 注意事項")
    for w in template.warnings:
        lines.append(f"- {w}")
    return "\n".join(lines)
