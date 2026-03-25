"""主要商取引法令のナレッジベース."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LawRequirement:
    law_id: str
    law_name: str
    category: str
    description: str
    key_requirements: list[str]
    applicable_industries: list[str] = field(default_factory=list)
    penalties: str = ""


JAPAN_COMMERCIAL_LAWS: list[LawRequirement] = [
    # 民法（契約関連）
    LawRequirement("CL01", "民法（契約総則）", "契約", "契約の成立・効力・解除に関する基本法", ["契約自由の原則", "信義誠実の原則", "公序良俗違反の無効", "錯誤による取消し", "詐欺・強迫による取消し"]),
    LawRequirement("CL02", "民法（債権）", "債権", "債権債務の発生・履行・消滅に関する規定", ["債務不履行責任", "損害賠償の範囲", "契約不適合責任（旧瑕疵担保）", "相殺", "消滅時効"]),
    # 商法
    LawRequirement("CL03", "商法", "商取引", "商人間の取引に関する特別法", ["商行為の迅速処理", "商事消滅時効5年", "商人間の留置権", "報酬請求権の推定"]),
    # 下請法
    LawRequirement("CL04", "下請代金支払遅延等防止法", "下請", "親事業者と下請事業者の取引適正化", ["書面の交付義務", "支払期日（60日以内）", "減額の禁止", "返品の禁止", "買いたたきの禁止", "報復措置の禁止"], ["manufacturing", "it"], "勧告・公表、50万円以下の罰金"),
    # 個人情報保護法
    LawRequirement("CL05", "個人情報保護法", "個人情報", "個人情報の適正な取扱いに関する法律", ["利用目的の特定・公表", "適正な取得", "安全管理措置", "第三者提供の制限", "本人の開示・訂正・利用停止請求権", "個人情報保護委員会への報告"], penalties="1年以下の懲役又は100万円以下の罰金"),
    # 消費者契約法
    LawRequirement("CL06", "消費者契約法", "消費者保護", "事業者と消費者間の契約の適正化", ["不当な勧誘による取消し", "不当な契約条項の無効", "事業者の損害賠償責任免除条項の無効", "消費者の利益を一方的に害する条項の無効"]),
    # 特定商取引法
    LawRequirement("CL07", "特定商取引法", "消費者保護", "訪問販売・通信販売等の取引規制", ["クーリングオフ制度", "広告表示義務", "誇大広告の禁止", "迷惑メールの禁止", "返品特約の表示義務"], penalties="業務停止命令、3年以下の懲役又は300万円以下の罰金"),
    # 不正競争防止法
    LawRequirement("CL08", "不正競争防止法", "競争法", "不正な競争行為の防止", ["営業秘密の保護", "商品等表示の混同防止", "信用毀損行為の禁止", "技術的制限手段の回避禁止"], penalties="10年以下の懲役又は2000万円以下の罰金"),
    # 独占禁止法
    LawRequirement("CL09", "独占禁止法", "競争法", "公正な競争の確保", ["私的独占の禁止", "不当な取引制限（カルテル）の禁止", "不公正な取引方法の禁止", "優越的地位の濫用禁止"], penalties="5年以下の懲役又は500万円以下の罰金"),
    # 電子契約法
    LawRequirement("CL10", "電子消費者契約法", "電子取引", "電子商取引における消費者保護", ["操作ミスによる契約の無効", "電子承諾通知の到達", "確認画面の設置義務"]),
    # 電気通信事業法
    LawRequirement("CL11", "電気通信事業法", "通信", "電気通信事業の規制", ["通信の秘密の保護", "個人情報の適正な取扱い", "利用者への契約条件説明義務"], ["it"]),
    # 資金決済法
    LawRequirement("CL12", "資金決済法", "金融", "前払式支払手段・資金移動業の規制", ["前払式支払手段の届出・登録", "供託義務", "利用者保護"], ["finance", "it"]),
    # 景品表示法
    LawRequirement("CL13", "景品表示法", "表示規制", "不当な表示・景品の規制", ["優良誤認表示の禁止", "有利誤認表示の禁止", "景品類の制限", "不実証広告規制"], penalties="措置命令、課徴金"),
    # 労働関連
    LawRequirement("CL14", "労働基準法", "労働", "労働条件の最低基準", ["労働時間の制限", "賃金の支払規制", "解雇の制限", "有給休暇"], penalties="6ヶ月以下の懲役又は30万円以下の罰金"),
    LawRequirement("CL15", "労働契約法", "労働", "労働契約の基本ルール", ["労働条件の明示", "就業規則の不利益変更制限", "雇止め法理", "無期転換ルール"]),
]


INDUSTRY_COMPLIANCE_MAP: dict[str, list[str]] = {
    "it": ["CL01", "CL02", "CL04", "CL05", "CL06", "CL07", "CL08", "CL10", "CL11", "CL13"],
    "finance": ["CL01", "CL02", "CL05", "CL06", "CL09", "CL12", "CL13"],
    "healthcare": ["CL01", "CL02", "CL05", "CL06", "CL13"],
    "retail": ["CL01", "CL02", "CL05", "CL06", "CL07", "CL09", "CL13"],
    "manufacturing": ["CL01", "CL02", "CL03", "CL04", "CL08", "CL09", "CL13"],
    "real_estate": ["CL01", "CL02", "CL05", "CL06", "CL07", "CL13"],
    "food": ["CL01", "CL02", "CL05", "CL06", "CL07", "CL13"],
    "education": ["CL01", "CL02", "CL05", "CL06", "CL13"],
    "other": ["CL01", "CL02", "CL05", "CL06", "CL13"],
}


def get_laws_for_industry(industry: str) -> list[LawRequirement]:
    law_ids = INDUSTRY_COMPLIANCE_MAP.get(industry, INDUSTRY_COMPLIANCE_MAP["other"])
    law_map = {law.law_id: law for law in JAPAN_COMMERCIAL_LAWS}
    return [law_map[lid] for lid in law_ids if lid in law_map]


def get_law_by_id(law_id: str) -> LawRequirement | None:
    for law in JAPAN_COMMERCIAL_LAWS:
        if law.law_id == law_id:
            return law
    return None
