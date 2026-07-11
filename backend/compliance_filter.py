"""
backend/compliance_filter.py
Regulatory compliance filter for MSL AI Copilot.
Flags off-label promotion, unsupported efficacy claims, and language
that violates FDA medical affairs guidance (21 CFR Part 202, PhRMA Code).
"""

import re
from dataclasses import dataclass, field
from enum import Enum


class FlagSeverity(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class ComplianceFlag:
    severity: FlagSeverity
    category: str
    matched_text: str
    explanation: str
    suggestion: str


@dataclass
class ComplianceReport:
    original_text: str
    flags: list = field(default_factory=list)
    is_compliant: bool = True
    risk_level: str = "LOW"
    summary: str = ""

    def add_flag(self, flag: ComplianceFlag):
        self.flags.append(flag)
        if flag.severity == FlagSeverity.HIGH:
            self.is_compliant = False
            self.risk_level = "HIGH"
        elif flag.severity == FlagSeverity.MEDIUM and self.risk_level != "HIGH":
            self.risk_level = "MEDIUM"

    def generate_summary(self):
        if not self.flags:
            self.summary = "No compliance issues detected."
        else:
            high = sum(1 for f in self.flags if f.severity == FlagSeverity.HIGH)
            med = sum(1 for f in self.flags if f.severity == FlagSeverity.MEDIUM)
            low = sum(1 for f in self.flags if f.severity == FlagSeverity.LOW)
            self.summary = (f"{len(self.flags)} flag(s): {high} HIGH, {med} MEDIUM, {low} LOW. "
                            f"Risk: {self.risk_level}")


OFF_LABEL_PATTERNS = [
    {
        "pattern": r"\b(superior to|better than|outperforms|more effective than)\b",
        "severity": FlagSeverity.HIGH,
        "category": "Comparative Efficacy Claim",
        "explanation": "Comparative superiority claims require head-to-head trial data and FDA approval.",
        "suggestion": "Use: 'In [study], [drug] demonstrated X vs Y.'",
    },
    {
        "pattern": r"\b(cure[sd]?|curative|eliminates? the disease|100% effective|guaranteed)\b",
        "severity": FlagSeverity.HIGH,
        "category": "Absolute Efficacy Claim",
        "explanation": "Absolute efficacy claims are prohibited without FDA approval.",
        "suggestion": "Use qualified language with study context.",
    },
    {
        "pattern": r"\b(you should prescribe|encourage .{0,20} to prescribe|increase prescribing)\b",
        "severity": FlagSeverity.HIGH,
        "category": "Prescribing Influence",
        "explanation": "Directing HCPs to prescribe crosses into sales promotion.",
        "suggestion": "Share data; let HCPs make independent decisions.",
    },
]

PROMOTIONAL_PATTERNS = [
    {
        "pattern": r"\b(breakthrough|revolutionary|game.?changer|miracle|groundbreaking)\b",
        "severity": FlagSeverity.MEDIUM,
        "category": "Promotional Language",
        "explanation": "Superlative marketing language is inappropriate in scientific exchange.",
        "suggestion": "Use specific, evidence-based language.",
    },
    {
        "pattern": r"\b(our drug|our product|our medication|our therapy)\b",
        "severity": FlagSeverity.MEDIUM,
        "category": "Possessive Product Language",
        "explanation": "MSL materials should reference drugs by name, not as 'ours'.",
        "suggestion": "Use the drug's brand or generic name.",
    },
]

SAFETY_PATTERNS = [
    {
        "pattern": r"\b(no side effects|completely safe|zero risk|no adverse events)\b",
        "severity": FlagSeverity.HIGH,
        "category": "Safety Minimization",
        "explanation": "Omitting safety information violates FDA fair balance requirements.",
        "suggestion": "Include relevant adverse event data alongside efficacy data.",
    },
    {
        "pattern": r"\b(negligible risk|ignore the side|don.t worry about)\b",
        "severity": FlagSeverity.MEDIUM,
        "category": "Risk Downplaying",
        "explanation": "Downplaying risks is inconsistent with fair balance communication.",
        "suggestion": "Present risk data objectively.",
    },
]

DATA_INTEGRITY_PATTERNS = [
    {
        "pattern": r"\b(studies show|research proves|science proves)\b",
        "severity": FlagSeverity.LOW,
        "category": "Unattributed Data Reference",
        "explanation": "Vague references to studies without citation are scientifically weak.",
        "suggestion": "Cite: 'In the Phase III TRIAL-NAME study (Author et al., Year)...'",
    },
    {
        "pattern": r"\b(unpublished data shows|based on my experience|I believe that)\b",
        "severity": FlagSeverity.MEDIUM,
        "category": "Unsupported Personal Claim",
        "explanation": "MSL communications must be grounded in peer-reviewed data.",
        "suggestion": "Reference only published, peer-reviewed or company-approved data.",
    },
]

ALL_PATTERNS = OFF_LABEL_PATTERNS + PROMOTIONAL_PATTERNS + SAFETY_PATTERNS + DATA_INTEGRITY_PATTERNS


def scan_text(text: str) -> ComplianceReport:
    """Scan text for compliance issues and return a ComplianceReport."""
    report = ComplianceReport(original_text=text)
    for pattern_def in ALL_PATTERNS:
        matches = re.finditer(pattern_def["pattern"], text, re.IGNORECASE)
        for match in matches:
            flag = ComplianceFlag(
                severity=pattern_def["severity"],
                category=pattern_def["category"],
                matched_text=match.group(0),
                explanation=pattern_def["explanation"],
                suggestion=pattern_def["suggestion"],
            )
            report.add_flag(flag)
    report.generate_summary()
    return report


def get_compliance_badge(report: ComplianceReport) -> tuple:
    """Return (color, label) for Streamlit display."""
    if report.risk_level == "HIGH":
        return ("red", "HIGH RISK - Review Required")
    elif report.risk_level == "MEDIUM":
        return ("orange", "MEDIUM RISK - Some Concerns")
    else:
        return ("green", "LOW RISK - Compliant")


def highlight_flags_in_text(text: str, flags: list) -> str:
    """Return HTML with flagged terms color-highlighted."""
    highlighted = text
    for flag in flags:
        color = {FlagSeverity.HIGH: "#ff4444", FlagSeverity.MEDIUM: "#ff9900",
                 FlagSeverity.LOW: "#ffcc00"}.get(flag.severity, "#ffcc00")
        highlighted = re.sub(
            re.escape(flag.matched_text),
            f'<mark style="background-color:{color};">{flag.matched_text}</mark>',
            highlighted, flags=re.IGNORECASE,
        )
    return highlighted


MSL_BEST_PRACTICES = [
    "Always cite specific studies with author, year, and journal",
    "Present efficacy and safety data together (fair balance)",
    "Use conditional language: 'data suggest' not 'data prove'",
    "Reference only approved indications unless responding to unsolicited off-label request",
    "Document unsolicited off-label requests separately",
    "Avoid comparative claims unless head-to-head trial data exists",
    "Never recommend specific prescribing decisions",
    "Ensure all shared materials are medically/legally approved",
]
