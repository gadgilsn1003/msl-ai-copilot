"""
🛡️ Compliance Filter - FDA Regulatory Compliance Scanner

Rule-based scanning aligned with FDA 21 CFR Part 202 and PhRMA Code.
Flags: off-label promotion, comparative efficacy claims, absolute claims,
safety minimization, promotional language.

Three-tier severity: HIGH / MEDIUM / LOW
"""

import re


# =================================================================================
# COMPLIANCE RULES
# =================================================================================
COMPLIANCE_RULES = [
    # HIGH SEVERITY - Off-label promotion
    {
        "id": "OFF_LABEL_001",
        "severity": "HIGH",
        "category": "Off-Label Promotion",
        "patterns": [
            r"\b(should be used for|recommended for|indicated for)\b.*(?!FDA.approved)",
            r"\b(off-label use is|can be used for)\b",
            r"\b(we recommend|we suggest using)\b",
        ],
        "message": "Potential off-label promotion detected. Ensure all efficacy claims are within approved indications.",
    },
    # HIGH SEVERITY - Comparative claims without data
    {
        "id": "COMP_001",
        "severity": "HIGH",
        "category": "Comparative Efficacy Claims",
        "patterns": [
            r"\b(superior to|better than|more effective than|outperforms)\b",
            r"\b(best in class|first in class|only treatment)\b",
            r"\b(preferred over|drug of choice)\b",
        ],
        "message": "Comparative efficacy claim detected. Ensure head-to-head data supports this claim.",
    },
    # HIGH SEVERITY - Absolute claims
    {
        "id": "ABS_001",
        "severity": "HIGH",
        "category": "Absolute Claims",
        "patterns": [
            r"\b(cures|eliminates|eradicates|guarantees)\b",
            r"\b(100% effective|completely safe|no side effects)\b",
            r"\b(always works|never fails|zero risk)\b",
        ],
        "message": "Absolute claim detected. Scientific communications should use qualified language.",
    },
    # MEDIUM SEVERITY - Safety minimization
    {
        "id": "SAFETY_001",
        "severity": "MEDIUM",
        "category": "Safety Minimization",
        "patterns": [
            r"\b(well.tolerated|excellent safety|benign side effect)\b",
            r"\b(minimal risk|negligible adverse|safe for all)\b",
            r"\b(no serious|no significant adverse)\b",
        ],
        "message": "Potential safety minimization. Ensure balanced presentation of safety data.",
    },
    # MEDIUM SEVERITY - Promotional language
    {
        "id": "PROMO_001",
        "severity": "MEDIUM",
        "category": "Promotional Language",
        "patterns": [
            r"\b(breakthrough|revolutionary|game.changing|miracle)\b",
            r"\b(transformative|unparalleled|unprecedented efficacy)\b",
            r"\b(amazing results|remarkable outcomes|extraordinary)\b",
        ],
        "message": "Promotional language detected. Use objective, evidence-based terminology.",
    },
    # LOW SEVERITY - Unqualified statements
    {
        "id": "QUAL_001",
        "severity": "LOW",
        "category": "Unqualified Statements",
        "patterns": [
            r"\b(proven to|demonstrated to|shown to)\b(?!.*\b(in a|in the|by)\b)",
            r"\b(clearly|obviously|undoubtedly|certainly)\b",
        ],
        "message": "Consider adding qualifiers or citing specific evidence to support this statement.",
    },
    # LOW SEVERITY - Missing context
    {
        "id": "CTX_001",
        "severity": "LOW",
        "category": "Missing Context",
        "patterns": [
            r"\b(studies show|research shows|data shows)\b(?!.*\b(et al|PMID|trial|study)\b)",
            r"\b(evidence suggests)\b(?!.*\b(from|in|based)\b)",
        ],
        "message": "Consider specifying which studies or data sources support this claim.",
    },
]


# =================================================================================
# SCREENING FUNCTION
# =================================================================================
def screen_content(content: str) -> dict:
    """
    Screen content for compliance issues.

    Args:
        content: Text content to screen

    Returns:
        Dictionary with:
            - passed: bool (True if no HIGH severity flags)
            - flags: list of flag dictionaries
            - summary: string summary of findings
            - score: compliance score (0-100)
    """
    if not content or content.strip() == "":
        return {
            "passed": True,
            "flags": [],
            "summary": "No content to screen.",
            "score": 100,
        }

    flags = []
    content_lower = content.lower()

    for rule in COMPLIANCE_RULES:
        for pattern in rule["patterns"]:
            try:
                matches = re.findall(pattern, content_lower)
                if matches:
                    # Get the first match for context
                    match = re.search(pattern, content_lower)
                    context = ""
                    if match:
                        start = max(0, match.start() - 30)
                        end = min(len(content), match.end() + 30)
                        context = content[start:end].strip()

                    flags.append({
                        "id": rule["id"],
                        "severity": rule["severity"],
                        "category": rule["category"],
                        "message": rule["message"],
                        "context": f"...{context}...",
                        "match_count": len(matches),
                    })
                    break  # One flag per rule is enough
            except re.error:
                continue

    # Calculate compliance score
    high_count = sum(1 for f in flags if f["severity"] == "HIGH")
    medium_count = sum(1 for f in flags if f["severity"] == "MEDIUM")
    low_count = sum(1 for f in flags if f["severity"] == "LOW")

    score = 100 - (high_count * 25) - (medium_count * 10) - (low_count * 5)
    score = max(0, min(100, score))

    # Determine pass/fail (fails only on HIGH severity)
    passed = high_count == 0

    # Generate summary
    if not flags:
        summary = "Content passed compliance screening. No issues detected."
    else:
        parts = []
        if high_count:
            parts.append(f"{high_count} HIGH severity issue(s)")
        if medium_count:
            parts.append(f"{medium_count} MEDIUM severity issue(s)")
        if low_count:
            parts.append(f"{low_count} LOW severity issue(s)")
        summary = f"Compliance screening found: {', '.join(parts)}."

    return {
        "passed": passed,
        "flags": flags,
        "summary": summary,
        "score": score,
        "counts": {
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
        },
    }


def get_compliance_badge(score: int) -> str:
    """
    Get a compliance badge based on score.

    Args:
        score: Compliance score (0-100)

    Returns:
        Badge string with emoji
    """
    if score >= 90:
        return "✅ Compliant"
    elif score >= 70:
        return "⚠️ Minor Issues"
    elif score >= 50:
        return "🟠 Review Needed"
    else:
        return "🔴 Non-Compliant"
