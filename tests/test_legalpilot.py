"""LegalPilot テスト."""


from app.models import (
    ContractReviewResult,
    GeneratedTerms,
    IndustryType,
    RiskLevel,
    ServiceInfo,
    ServiceType,
)
from app.services.contract_reviewer import (
    _determine_overall_risk,
    get_risk_summary_by_type,
    review_contract,
)
from app.services.compliance_checker import (
    ComplianceInput,
    check_compliance,
    get_supported_industries,
)
from app.services.terms_generator import generate_terms
from app.services.template_library import (
    get_contract_template,
    get_template_sections,
    list_available_templates,
    search_templates,
)
from app.services.law_alert import (
    get_alert_summary,
    get_alerts_by_impact,
    get_alerts_for_industry,
    get_all_alerts,
)
from app.knowledge.contract_risks import (
    CONTRACT_RISK_PATTERNS,
    get_all_risk_types,
)
from app.knowledge.japan_laws import (
    JAPAN_COMMERCIAL_LAWS,
    get_law_by_id,
    get_laws_for_industry,
)
from app.knowledge.contract_templates import (
    get_all_template_types,
    get_template,
    get_template_text,
)


# ===========================================================================
# Contract Reviewer Tests
# ===========================================================================

RISKY_CONTRACT = """
業務委託契約書

第1条 甲は乙に対し、本業務に関する一切の損害を無制限に賠償する義務を負う。
第2条 甲は理由なくいつでも解除することができる。乙は解除できない。
第3条 成果物の著作権を譲渡し、著作者人格権を行使しない。
第4条 秘密情報は永久に開示してはならない。
第5条 報酬は別途協議する。
第6条 甲は乙の下請として製造委託を行う。検収後90日以内に支払う。
第7条 乙はいかなる場合も一切の責任を負わないものとする。
"""

SAFE_CONTRACT = """
業務委託契約書

第1条 業務内容を明確に定める。
第2条 報酬は月額100万円とし、毎月末締め翌月15日払いとする。
第3条 本契約の有効期間は1年間とする。
"""


class TestContractReviewer:
    def test_risky_contract_has_findings(self) -> None:
        result = review_contract(RISKY_CONTRACT)
        assert isinstance(result, ContractReviewResult)
        assert len(result.risk_clauses) > 0

    def test_risky_contract_has_critical(self) -> None:
        result = review_contract(RISKY_CONTRACT)
        assert result.critical_count > 0

    def test_risky_contract_overall_critical(self) -> None:
        result = review_contract(RISKY_CONTRACT)
        assert result.overall_risk in (RiskLevel.CRITICAL, RiskLevel.HIGH)

    def test_safe_contract_fewer_issues(self) -> None:
        result = review_contract(SAFE_CONTRACT)
        assert result.critical_count == 0

    def test_empty_contract(self) -> None:
        result = review_contract("")
        assert len(result.risk_clauses) == 0
        assert result.overall_risk == RiskLevel.INFO

    def test_sorted_by_risk(self) -> None:
        result = review_contract(RISKY_CONTRACT)
        risk_order = {RiskLevel.CRITICAL: 0, RiskLevel.HIGH: 1, RiskLevel.MEDIUM: 2, RiskLevel.LOW: 3, RiskLevel.INFO: 4}
        levels = [risk_order[r.risk_level] for r in result.risk_clauses]
        assert levels == sorted(levels)

    def test_summary_not_empty(self) -> None:
        result = review_contract(RISKY_CONTRACT)
        assert len(result.summary) > 0

    def test_recommendations_not_empty(self) -> None:
        result = review_contract(RISKY_CONTRACT)
        assert len(result.recommendations) > 0

    def test_risk_summary_by_type(self) -> None:
        result = review_contract(RISKY_CONTRACT)
        summary = get_risk_summary_by_type(result)
        assert isinstance(summary, dict)

    def test_determine_overall_risk_no_clauses(self) -> None:
        assert _determine_overall_risk([]) == RiskLevel.INFO


# ===========================================================================
# Compliance Checker Tests
# ===========================================================================

class TestComplianceChecker:
    def test_it_industry(self) -> None:
        inp = ComplianceInput(industry=IndustryType.IT)
        result = check_compliance(inp)
        assert result.industry == IndustryType.IT
        assert result.non_compliant_count > 0

    def test_all_compliant(self) -> None:
        inp = ComplianceInput(
            industry=IndustryType.IT,
            has_privacy_policy=True, has_terms_of_service=True,
            has_proper_contracts=True, has_subcontract_compliance=True,
            has_ip_management=True, has_data_security=True,
            has_consumer_protection=True,
        )
        result = check_compliance(inp)
        assert result.score > 50.0

    def test_finance_industry(self) -> None:
        inp = ComplianceInput(industry=IndustryType.FINANCE)
        result = check_compliance(inp)
        assert len(result.items) > 0

    def test_manufacturing_industry(self) -> None:
        inp = ComplianceInput(industry=IndustryType.MANUFACTURING)
        result = check_compliance(inp)
        assert len(result.items) > 0

    def test_score_0_to_100(self) -> None:
        inp = ComplianceInput(industry=IndustryType.RETAIL)
        result = check_compliance(inp)
        assert 0.0 <= result.score <= 100.0

    def test_summary_not_empty(self) -> None:
        inp = ComplianceInput(industry=IndustryType.IT)
        result = check_compliance(inp)
        assert len(result.summary) > 0

    def test_supported_industries(self) -> None:
        industries = get_supported_industries()
        assert "it" in industries
        assert "finance" in industries


# ===========================================================================
# Terms Generator Tests
# ===========================================================================

class TestTermsGenerator:
    def test_basic_generation(self) -> None:
        info = ServiceInfo(service_name="TestApp", service_type=ServiceType.WEB_SERVICE, company_name="テスト株式会社")
        result = generate_terms(info)
        assert isinstance(result, GeneratedTerms)

    def test_tos_contains_service_name(self) -> None:
        info = ServiceInfo(service_name="MyService", service_type=ServiceType.SAAS, company_name="MyCompany")
        result = generate_terms(info)
        assert "MyService" in result.terms_of_service

    def test_pp_contains_company_name(self) -> None:
        info = ServiceInfo(service_name="TestApp", service_type=ServiceType.WEB_SERVICE, company_name="テスト会社")
        result = generate_terms(info)
        assert "テスト会社" in result.privacy_policy

    def test_paid_features_section(self) -> None:
        info = ServiceInfo(service_name="T", service_type=ServiceType.SAAS, company_name="C", has_paid_features=True)
        result = generate_terms(info)
        assert "有料サービス" in result.terms_of_service
        assert "決済" in result.privacy_policy

    def test_minor_section(self) -> None:
        info = ServiceInfo(service_name="T", service_type=ServiceType.WEB_SERVICE, company_name="C", target_minors=True)
        result = generate_terms(info)
        assert "未成年" in result.terms_of_service

    def test_international_section(self) -> None:
        info = ServiceInfo(service_name="T", service_type=ServiceType.WEB_SERVICE, company_name="C", international=True)
        result = generate_terms(info)
        assert "国際" in result.privacy_policy or "国外" in result.privacy_policy

    def test_cookie_section(self) -> None:
        info = ServiceInfo(service_name="T", service_type=ServiceType.WEB_SERVICE, company_name="C", uses_cookies=True)
        result = generate_terms(info)
        assert "Cookie" in result.privacy_policy

    def test_summary_not_empty(self) -> None:
        info = ServiceInfo(service_name="T", service_type=ServiceType.EC_SITE, company_name="C")
        result = generate_terms(info)
        assert len(result.summary) > 0


# ===========================================================================
# Template Library Tests
# ===========================================================================

class TestTemplateLibrary:
    def test_list_templates(self) -> None:
        templates = list_available_templates()
        assert len(templates) == 10

    def test_get_nda_template(self) -> None:
        t = get_contract_template("nda")
        assert t is not None
        assert "秘密保持" in t.name

    def test_get_all_types(self) -> None:
        for ttype in ["nda", "service_agreement", "sales", "license", "employment",
                       "lease", "consulting", "subcontracting", "joint_venture", "franchise"]:
            t = get_contract_template(ttype)
            assert t is not None, f"Template {ttype} not found"

    def test_template_has_text(self) -> None:
        t = get_contract_template("nda")
        assert t is not None
        assert len(t.template_text) > 0

    def test_template_has_key_points(self) -> None:
        t = get_contract_template("service_agreement")
        assert t is not None
        assert len(t.key_points) > 0

    def test_template_has_warnings(self) -> None:
        t = get_contract_template("employment")
        assert t is not None
        assert len(t.warnings) > 0

    def test_search_templates(self) -> None:
        results = search_templates("秘密")
        assert len(results) > 0

    def test_search_no_results(self) -> None:
        results = search_templates("zzznonexistent")
        assert len(results) == 0

    def test_get_template_sections(self) -> None:
        sections = get_template_sections("nda")
        assert len(sections) > 0

    def test_nonexistent_template(self) -> None:
        t = get_contract_template("nonexistent")
        assert t is None


# ===========================================================================
# Law Alert Tests
# ===========================================================================

class TestLawAlert:
    def test_it_alerts(self) -> None:
        alerts = get_alerts_for_industry(IndustryType.IT)
        assert len(alerts) > 0

    def test_finance_alerts(self) -> None:
        alerts = get_alerts_for_industry(IndustryType.FINANCE)
        assert len(alerts) > 0

    def test_healthcare_alerts(self) -> None:
        alerts = get_alerts_for_industry(IndustryType.HEALTHCARE)
        assert len(alerts) > 0

    def test_sorted_by_impact(self) -> None:
        alerts = get_alerts_for_industry(IndustryType.IT)
        risk_order = {RiskLevel.CRITICAL: 0, RiskLevel.HIGH: 1, RiskLevel.MEDIUM: 2, RiskLevel.LOW: 3, RiskLevel.INFO: 4}
        levels = [risk_order[a.impact_level] for a in alerts]
        assert levels == sorted(levels)

    def test_all_alerts(self) -> None:
        alerts = get_all_alerts()
        assert len(alerts) >= 10

    def test_alerts_by_impact_high(self) -> None:
        alerts = get_alerts_by_impact(RiskLevel.HIGH)
        assert all(a.impact_level in (RiskLevel.CRITICAL, RiskLevel.HIGH) for a in alerts)

    def test_alert_has_action_items(self) -> None:
        alerts = get_alerts_for_industry(IndustryType.IT)
        for a in alerts:
            assert len(a.action_items) > 0

    def test_alert_summary(self) -> None:
        summary = get_alert_summary(IndustryType.IT)
        assert isinstance(summary, dict)


# ===========================================================================
# Knowledge Base Tests
# ===========================================================================

class TestKnowledgeBase:
    def test_risk_patterns_count(self) -> None:
        assert len(CONTRACT_RISK_PATTERNS) >= 30

    def test_risk_types(self) -> None:
        types = get_all_risk_types()
        assert len(types) > 0

    def test_japan_laws_count(self) -> None:
        assert len(JAPAN_COMMERCIAL_LAWS) >= 10

    def test_get_law_by_id(self) -> None:
        law = get_law_by_id("CL01")
        assert law is not None
        assert "民法" in law.law_name

    def test_get_laws_for_it(self) -> None:
        laws = get_laws_for_industry("it")
        assert len(laws) > 0

    def test_template_types(self) -> None:
        types = get_all_template_types()
        assert len(types) == 10

    def test_template_text_generation(self) -> None:
        t = get_template("nda")
        assert t is not None
        text = get_template_text(t)
        assert "秘密保持" in text
