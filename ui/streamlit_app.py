"""LegalPilot Streamlit UI - 法務コンサルAI."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from app.models import IndustryType, ServiceInfo, ServiceType
from app.services.compliance_checker import ComplianceInput, check_compliance
from app.services.contract_reviewer import review_contract
from app.services.law_alert import get_alerts_for_industry
from app.services.template_library import get_contract_template, list_available_templates
from app.services.terms_generator import generate_terms

st.set_page_config(page_title="LegalPilot", page_icon="⚖️", layout="wide")

INDUSTRY_OPTIONS = {i.value: i for i in IndustryType}


def page_contract_review() -> None:
    st.header("契約書レビューAI")
    text = st.text_area("契約書テキスト", height=300, placeholder="契約書をここに貼り付け...")
    if st.button("レビュー実行") and text.strip():
        result = review_contract(text)
        st.markdown(f"**{result.summary}**")
        for r in result.risk_clauses:
            color = {"critical": "red", "high": "orange", "medium": "blue"}.get(r.risk_level.value, "gray")
            st.markdown(f":{color}[**{r.risk_level.value.upper()}**] {r.risk_type}: {r.description}")
            st.markdown(f"  → {r.suggestion}")


def page_compliance() -> None:
    st.header("コンプライアンスチェック")
    industry = st.selectbox("業種", list(INDUSTRY_OPTIONS.keys()))
    col1, col2 = st.columns(2)
    with col1:
        pp = st.checkbox("プライバシーポリシーあり")
        tos = st.checkbox("利用規約あり")
        contracts = st.checkbox("適正な契約書あり")
        subcontract = st.checkbox("下請法対応済")
        ip = st.checkbox("知財管理あり")
    with col2:
        anti_mono = st.checkbox("独禁法対応済")
        consumer = st.checkbox("消費者保護対応済")
        security = st.checkbox("データセキュリティ対応済")
        handbook = st.checkbox("就業規則あり")
        whistle = st.checkbox("通報制度あり")
    if st.button("チェック実行"):
        inp = ComplianceInput(industry=INDUSTRY_OPTIONS[industry], has_privacy_policy=pp, has_terms_of_service=tos, has_proper_contracts=contracts, has_subcontract_compliance=subcontract, has_ip_management=ip, has_anti_monopoly_compliance=anti_mono, has_consumer_protection=consumer, has_data_security=security, has_employee_handbook=handbook, has_whistleblower_system=whistle)
        result = check_compliance(inp)
        st.markdown(f"**{result.summary}**")
        st.metric("スコア", f"{result.score:.1f}/100")


def page_terms() -> None:
    st.header("利用規約・プライバシーポリシー生成")
    sname = st.text_input("サービス名", "MyService")
    cname = st.text_input("会社名", "テスト株式会社")
    stype = st.selectbox("サービス種別", [t.value for t in ServiceType])
    paid = st.checkbox("有料機能あり")
    cookies = st.checkbox("Cookie使用", value=True)
    if st.button("生成"):
        info = ServiceInfo(service_name=sname, service_type=ServiceType(stype), company_name=cname, has_paid_features=paid, uses_cookies=cookies)
        result = generate_terms(info)
        st.subheader("利用規約")
        st.text_area("", result.terms_of_service, height=300)
        st.subheader("プライバシーポリシー")
        st.text_area("", result.privacy_policy, height=300)


def page_templates() -> None:
    st.header("契約テンプレートライブラリ")
    templates = list_available_templates()
    choice = st.selectbox("テンプレート選択", [t["name"] for t in templates])
    ttype = next(t["type"] for t in templates if t["name"] == choice)
    t = get_contract_template(ttype)
    if t:
        st.markdown(t.template_text)
        st.subheader("留意事項")
        for kp in t.key_points:
            st.markdown(f"- {kp}")


def page_law_alerts() -> None:
    st.header("法改正アラート")
    industry = st.selectbox("業種", list(INDUSTRY_OPTIONS.keys()), key="alert_ind")
    alerts = get_alerts_for_industry(INDUSTRY_OPTIONS[industry])
    for a in alerts:
        color = {"critical": "red", "high": "orange", "medium": "blue"}.get(a.impact_level.value, "gray")
        st.markdown(f":{color}[**{a.impact_level.value.upper()}**] {a.law_name}")
        st.markdown(f"  {a.description}")
        st.markdown(f"  施行日: {a.effective_date}")


def main() -> None:
    st.sidebar.title("LegalPilot")
    pages = {"契約書レビュー": page_contract_review, "コンプライアンス": page_compliance, "利用規約生成": page_terms, "テンプレート": page_templates, "法改正アラート": page_law_alerts}
    page = st.sidebar.radio("メニュー", list(pages.keys()))
    pages[page]()


if __name__ == "__main__":
    main()
