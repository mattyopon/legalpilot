"""LegalPilot data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class RiskLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IndustryType(Enum):
    IT = "it"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    REAL_ESTATE = "real_estate"
    FOOD = "food"
    EDUCATION = "education"
    OTHER = "other"


class ContractType(Enum):
    NDA = "nda"
    SERVICE_AGREEMENT = "service_agreement"
    SALES = "sales"
    LICENSE = "license"
    EMPLOYMENT = "employment"
    LEASE = "lease"
    CONSULTING = "consulting"
    SUBCONTRACTING = "subcontracting"
    JOINT_VENTURE = "joint_venture"
    FRANCHISE = "franchise"


class ServiceType(Enum):
    WEB_SERVICE = "web_service"
    MOBILE_APP = "mobile_app"
    EC_SITE = "ec_site"
    SAAS = "saas"
    PLATFORM = "platform"
    OTHER = "other"


@dataclass
class RiskClause:
    clause_text: str
    risk_type: str
    risk_level: RiskLevel
    description: str
    suggestion: str
    legal_basis: str = ""


@dataclass
class ContractReviewResult:
    contract_text: str
    risk_clauses: list[RiskClause]
    overall_risk: RiskLevel
    summary: str
    recommendations: list[str] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for r in self.risk_clauses if r.risk_level == RiskLevel.CRITICAL)

    @property
    def high_count(self) -> int:
        return sum(1 for r in self.risk_clauses if r.risk_level == RiskLevel.HIGH)


@dataclass
class ComplianceCheckItem:
    category: str
    item_name: str
    description: str
    is_compliant: bool
    risk_level: RiskLevel
    recommendation: str
    legal_basis: str = ""


@dataclass
class ComplianceCheckResult:
    industry: IndustryType
    items: list[ComplianceCheckItem]
    score: float
    summary: str

    @property
    def non_compliant_count(self) -> int:
        return sum(1 for i in self.items if not i.is_compliant)


@dataclass
class ServiceInfo:
    service_name: str
    service_type: ServiceType
    company_name: str
    collects_personal_data: bool = True
    uses_cookies: bool = True
    has_paid_features: bool = False
    target_minors: bool = False
    international: bool = False


@dataclass
class GeneratedTerms:
    service_info: ServiceInfo
    terms_of_service: str
    privacy_policy: str
    summary: str


@dataclass
class ContractTemplate:
    contract_type: ContractType
    name: str
    description: str
    template_text: str
    key_points: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class LawAlert:
    law_name: str
    alert_type: str
    description: str
    impact_level: RiskLevel
    affected_industries: list[IndustryType]
    effective_date: str
    action_items: list[str] = field(default_factory=list)
    source: str = ""
