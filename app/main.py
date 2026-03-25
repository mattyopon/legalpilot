"""LegalPilot FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.models import IndustryType, ServiceType
from app.services.compliance_checker import ComplianceInput, check_compliance
from app.services.contract_reviewer import review_contract
from app.services.law_alert import get_alerts_for_industry
from app.services.template_library import get_contract_template, list_available_templates
from app.services.terms_generator import generate_terms
from app.models import ServiceInfo

app = FastAPI(title="LegalPilot", description="法務コンサルAI", version="1.0.0")


class ContractReviewRequest(BaseModel):
    contract_text: str = Field(..., description="契約書テキスト")


class ComplianceCheckRequest(BaseModel):
    industry: str = Field(..., description="業種")
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


class TermsGenerateRequest(BaseModel):
    service_name: str = Field(..., description="サービス名")
    service_type: str = Field("web_service", description="サービス種別")
    company_name: str = Field(..., description="会社名")
    collects_personal_data: bool = True
    uses_cookies: bool = True
    has_paid_features: bool = False
    target_minors: bool = False
    international: bool = False


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "LegalPilot", "version": "1.0.0", "status": "running"}


@app.post("/api/contract/review")
def api_review_contract(request: ContractReviewRequest) -> dict[str, object]:
    if not request.contract_text.strip():
        raise HTTPException(status_code=400, detail="契約書テキストが空です")
    result = review_contract(request.contract_text)
    return {
        "summary": result.summary,
        "overall_risk": result.overall_risk.value,
        "risk_clauses": [
            {"clause_text": r.clause_text, "risk_type": r.risk_type, "risk_level": r.risk_level.value,
             "description": r.description, "suggestion": r.suggestion}
            for r in result.risk_clauses
        ],
        "recommendations": result.recommendations,
    }


@app.post("/api/compliance/check")
def api_check_compliance(request: ComplianceCheckRequest) -> dict[str, object]:
    input_data = ComplianceInput(
        industry=IndustryType(request.industry),
        has_privacy_policy=request.has_privacy_policy,
        has_terms_of_service=request.has_terms_of_service,
        has_proper_contracts=request.has_proper_contracts,
        has_subcontract_compliance=request.has_subcontract_compliance,
        has_anti_monopoly_compliance=request.has_anti_monopoly_compliance,
        has_consumer_protection=request.has_consumer_protection,
        has_ip_management=request.has_ip_management,
        has_data_security=request.has_data_security,
        has_employee_handbook=request.has_employee_handbook,
        has_whistleblower_system=request.has_whistleblower_system,
    )
    result = check_compliance(input_data)
    return {
        "summary": result.summary,
        "score": result.score,
        "items": [
            {"category": i.category, "item_name": i.item_name, "is_compliant": i.is_compliant,
             "risk_level": i.risk_level.value, "recommendation": i.recommendation}
            for i in result.items
        ],
    }


@app.post("/api/terms/generate")
def api_generate_terms(request: TermsGenerateRequest) -> dict[str, object]:
    info = ServiceInfo(
        service_name=request.service_name,
        service_type=ServiceType(request.service_type),
        company_name=request.company_name,
        collects_personal_data=request.collects_personal_data,
        uses_cookies=request.uses_cookies,
        has_paid_features=request.has_paid_features,
        target_minors=request.target_minors,
        international=request.international,
    )
    result = generate_terms(info)
    return {
        "summary": result.summary,
        "terms_of_service": result.terms_of_service,
        "privacy_policy": result.privacy_policy,
    }


@app.get("/api/templates")
def api_list_templates() -> dict[str, object]:
    return {"templates": list_available_templates()}


@app.get("/api/templates/{contract_type}")
def api_get_template(contract_type: str) -> dict[str, object]:
    template = get_contract_template(contract_type)
    if template is None:
        raise HTTPException(status_code=404, detail="テンプレートが見つかりません")
    return {
        "name": template.name,
        "description": template.description,
        "template_text": template.template_text,
        "key_points": template.key_points,
        "warnings": template.warnings,
    }


@app.get("/api/law-alerts/{industry}")
def api_get_law_alerts(industry: str) -> dict[str, object]:
    alerts = get_alerts_for_industry(IndustryType(industry))
    return {
        "industry": industry,
        "alerts": [
            {"law_name": a.law_name, "alert_type": a.alert_type, "description": a.description,
             "impact_level": a.impact_level.value, "effective_date": a.effective_date,
             "action_items": a.action_items}
            for a in alerts
        ],
    }
