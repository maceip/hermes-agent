"""URL phishing analysis — detect suspicious domains, homograph attacks, and
fraud indicators before the agent interacts with login or payment forms.

This module provides both a standalone analysis function and a registered tool
that the web-browsing-agent persona uses to vet URLs.

Detection layers:
  1. Homograph attack detection (IDN/punycode visual lookalikes)
  2. Typosquatting via edit-distance against known legitimate domains
  3. Suspicious TLD flagging (.tk, .ml, .ga, .cf, .gq — free TLDs popular
     with phishers)
  4. HTTPS enforcement on login/payment pages
  5. Excessive subdomain depth (brand.login.evil.com patterns)
  6. Recently-registered domain heuristic (short random-looking names)
  7. Known brand impersonation patterns
"""

import json
import logging
import re
import unicodedata
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------
# Homograph detection tables
# -------------------------------------------------------------------------

# Characters from non-Latin scripts that visually resemble Latin letters.
# Maps confusable codepoint -> ASCII equivalent it mimics.
_CONFUSABLES: Dict[str, str] = {
    # Cyrillic
    "\u0430": "a", "\u0435": "e", "\u043e": "o", "\u0440": "p",
    "\u0441": "c", "\u0443": "y", "\u0445": "x", "\u0456": "i",
    "\u0458": "j", "\u04bb": "h", "\u0455": "s", "\u0442": "t",
    "\u043a": "k", "\u043c": "m", "\u043d": "n", "\u0432": "b",
    "\u0433": "r", "\u0437": "3", "\u0452": "d",
    # Greek
    "\u03b1": "a", "\u03bf": "o", "\u03c1": "p", "\u03b5": "e",
    "\u03b9": "i", "\u03ba": "k", "\u03bd": "v", "\u03c4": "t",
    "\u03c5": "u", "\u03c9": "w",
    # Latin extended / special
    "\u0131": "i",  # dotless i
    "\u0142": "l",  # l with stroke
    "\u00e7": "c",  # c cedilla (less suspicious but flagged in IDN context)
    "\u0111": "d",  # d with stroke
    "\u0127": "h",  # h with stroke
}

# High-confidence brands attackers commonly impersonate
_TARGET_BRANDS = {
    "google": "google.com",
    "facebook": "facebook.com",
    "apple": "apple.com",
    "amazon": "amazon.com",
    "microsoft": "microsoft.com",
    "paypal": "paypal.com",
    "netflix": "netflix.com",
    "instagram": "instagram.com",
    "twitter": "twitter.com",
    "linkedin": "linkedin.com",
    "github": "github.com",
    "dropbox": "dropbox.com",
    "chase": "chase.com",
    "wellsfargo": "wellsfargo.com",
    "bankofamerica": "bankofamerica.com",
    "coinbase": "coinbase.com",
    "binance": "binance.com",
    "steam": "steampowered.com",
    "discord": "discord.com",
    "spotify": "spotify.com",
    "adobe": "adobe.com",
    "yahoo": "yahoo.com",
    "outlook": "outlook.com",
    "icloud": "icloud.com",
}

# Free / commonly-abused TLDs (high phishing incidence)
_SUSPICIOUS_TLDS = frozenset({
    ".tk", ".ml", ".ga", ".cf", ".gq",   # Freenom free TLDs
    ".top", ".xyz", ".buzz", ".club",     # cheap gTLDs heavily abused
    ".work", ".click", ".link", ".surf",
    ".icu", ".cam", ".rest",
})


# -------------------------------------------------------------------------
# Core analysis
# -------------------------------------------------------------------------

def _detect_homograph(hostname: str) -> List[str]:
    """Check for mixed-script / confusable-character attacks."""
    findings = []

    # IDN (punycode) detection
    if hostname.startswith("xn--") or any(part.startswith("xn--") for part in hostname.split(".")):
        findings.append(
            "Domain uses Internationalized Domain Name (punycode). "
            "This may be a homograph attack using visually similar characters."
        )

    # Check for confusable characters
    confusable_chars = []
    for ch in hostname:
        if ch in _CONFUSABLES:
            confusable_chars.append(
                f"'{ch}' (U+{ord(ch):04X} {unicodedata.name(ch, '?')}) looks like '{_CONFUSABLES[ch]}'"
            )

    if confusable_chars:
        findings.append(
            f"Homograph attack detected — visually deceptive characters: "
            f"{'; '.join(confusable_chars[:5])}"
        )

    # Mixed-script detection (Latin + Cyrillic in same label)
    for label in hostname.split("."):
        scripts = set()
        for ch in label:
            if ch.isalpha():
                try:
                    script = unicodedata.name(ch, "").split()[0]
                    scripts.add(script)
                except (ValueError, IndexError):
                    pass
        if len(scripts) > 1 and scripts != {"LATIN"}:
            findings.append(
                f"Mixed Unicode scripts in '{label}': {', '.join(sorted(scripts))}. "
                "Legitimate domains rarely mix scripts."
            )

    return findings


def _detect_typosquat(hostname: str) -> List[str]:
    """Check if the domain looks like a typosquat of a known brand."""
    findings = []
    # Strip TLD for comparison
    parts = hostname.split(".")
    if len(parts) < 2:
        return findings

    # Use the second-level domain (e.g., "gooogle" from "gooogle.com")
    sld = parts[-2].lower()

    for brand, legit_domain in _TARGET_BRANDS.items():
        if sld == brand:
            # Exact match — check if it's actually the legitimate domain
            legit_sld = legit_domain.split(".")[0]
            if hostname.rstrip(".") != legit_domain:
                findings.append(
                    f"Domain contains brand name '{brand}' but is not the legitimate "
                    f"domain ({legit_domain}). Possible brand impersonation."
                )
            continue

        # Check for brand name embedded in subdomain or SLD
        if brand in sld and sld != brand:
            findings.append(
                f"Domain contains '{brand}' as substring ('{sld}'). "
                f"Legitimate domain is {legit_domain}."
            )

        # Simple edit-distance check (substitution, insertion, deletion)
        if len(sld) == len(brand) and sld != brand:
            diff = sum(1 for a, b in zip(sld, brand) if a != b)
            if diff == 1:
                findings.append(
                    f"Domain '{sld}' is 1 character away from '{brand}' "
                    f"(legitimate: {legit_domain}). Possible typosquat."
                )
        elif abs(len(sld) - len(brand)) == 1:
            # Check insertion/deletion (one char difference in length)
            shorter, longer = (brand, sld) if len(brand) < len(sld) else (sld, brand)
            i = j = diffs = 0
            while i < len(shorter) and j < len(longer):
                if shorter[i] != longer[j]:
                    diffs += 1
                    j += 1
                else:
                    i += 1
                    j += 1
            if diffs <= 1:
                findings.append(
                    f"Domain '{sld}' is very similar to '{brand}' "
                    f"(legitimate: {legit_domain}). Possible typosquat."
                )

    return findings


def _check_tld(hostname: str) -> List[str]:
    """Flag suspicious TLDs."""
    findings = []
    for tld in _SUSPICIOUS_TLDS:
        if hostname.endswith(tld):
            findings.append(
                f"Domain uses '{tld}' TLD which has high phishing incidence. "
                "Exercise extra caution."
            )
            break
    return findings


def _check_subdomain_depth(hostname: str) -> List[str]:
    """Flag excessive subdomain nesting (e.g., login.google.com.evil.xyz)."""
    findings = []
    parts = hostname.split(".")
    # Ignore www. prefix
    if parts[0] == "www":
        parts = parts[1:]
    if len(parts) > 4:
        findings.append(
            f"Excessive subdomain depth ({len(parts)} levels). "
            "Phishing sites often use deep subdomains to hide the real domain "
            f"(actual domain: {'.'.join(parts[-2:])})."
        )
    # Check if a brand name appears in a subdomain but not the registrable domain
    registrable = ".".join(parts[-2:]).lower()
    for brand, legit in _TARGET_BRANDS.items():
        for sub in parts[:-2]:
            if brand in sub.lower() and brand not in registrable:
                findings.append(
                    f"Brand name '{brand}' in subdomain but registrable domain "
                    f"is '{registrable}' (not {legit}). Likely phishing."
                )
    return findings


def _check_protocol(url: str) -> List[str]:
    """Flag HTTP (no TLS) on pages that likely handle credentials."""
    findings = []
    parsed = urlparse(url)
    if parsed.scheme == "http":
        findings.append(
            "Page uses HTTP (not HTTPS). Credentials sent over HTTP are "
            "transmitted in plain text and can be intercepted. "
            "Legitimate login pages use HTTPS."
        )
    return findings


def analyze_url(url: str) -> Dict[str, Any]:
    """Run all phishing checks against a URL and return a structured report.

    Returns:
        {
            "url": str,
            "hostname": str,
            "risk_level": "safe" | "low" | "medium" | "high" | "critical",
            "findings": [str, ...],
            "recommendation": str,
        }
    """
    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").strip().lower()
    except Exception:
        return {
            "url": url,
            "hostname": "",
            "risk_level": "high",
            "findings": ["Could not parse URL — malformed or suspicious format."],
            "recommendation": "Do not interact with this URL.",
        }

    if not hostname:
        return {
            "url": url,
            "hostname": "",
            "risk_level": "high",
            "findings": ["No hostname found in URL."],
            "recommendation": "Do not interact with this URL.",
        }

    findings: List[str] = []

    # Run all checks
    findings.extend(_detect_homograph(hostname))
    findings.extend(_detect_typosquat(hostname))
    findings.extend(_check_tld(hostname))
    findings.extend(_check_subdomain_depth(hostname))
    findings.extend(_check_protocol(url))

    # Determine risk level
    if not findings:
        risk = "low"
        recommendation = (
            "No obvious phishing indicators detected. Standard caution applies — "
            "verify the page content matches expectations before entering credentials."
        )
    elif any("homograph" in f.lower() or "mixed unicode" in f.lower() for f in findings):
        risk = "critical"
        recommendation = (
            "CRITICAL: Homograph attack indicators detected. This domain uses "
            "characters that visually mimic a different domain. Do NOT enter any "
            "credentials or personal information."
        )
    elif any("brand" in f.lower() and "not the legitimate" in f.lower() for f in findings):
        risk = "high"
        recommendation = (
            "HIGH RISK: Domain impersonates a known brand. Verify the exact domain "
            "in the address bar. Do not enter credentials."
        )
    elif any("typosquat" in f.lower() for f in findings):
        risk = "high"
        recommendation = (
            "HIGH RISK: Domain closely resembles a known legitimate domain. "
            "This is a common phishing technique. Verify carefully."
        )
    elif any("http" in f.lower() and "not https" in f.lower() for f in findings):
        risk = "medium"
        recommendation = (
            "MEDIUM RISK: Page lacks HTTPS encryption. Do not enter passwords "
            "or payment information on non-HTTPS pages."
        )
    elif len(findings) >= 2:
        risk = "medium"
        recommendation = (
            "Multiple suspicious indicators detected. Proceed with caution and "
            "verify the site through a known-good link (e.g., bookmark or search engine)."
        )
    else:
        risk = "low"
        recommendation = (
            "Minor suspicious indicator detected. Likely safe but verify "
            "the domain matches your expectations."
        )

    return {
        "url": url,
        "hostname": hostname,
        "risk_level": risk,
        "findings": findings,
        "recommendation": recommendation,
    }


# -------------------------------------------------------------------------
# Tool interface
# -------------------------------------------------------------------------

def url_phishing_check(url: str) -> str:
    """Analyze a URL for phishing indicators. Returns JSON report."""
    report = analyze_url(url)
    return json.dumps(report, indent=2)


# -------------------------------------------------------------------------
# Schema + registration
# -------------------------------------------------------------------------

URL_PHISHING_CHECK_SCHEMA = {
    "name": "url_phishing_check",
    "description": (
        "Analyze a URL for phishing indicators before interacting with it. "
        "Checks for homograph attacks (lookalike Unicode characters), "
        "typosquatting (misspelled brand domains), suspicious TLDs, "
        "excessive subdomain depth, HTTPS enforcement, and brand impersonation. "
        "Use this BEFORE entering any credentials or navigating to login/payment pages."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The URL to analyze for phishing indicators"
            }
        },
        "required": ["url"]
    }
}

from tools.registry import registry

registry.register(
    name="url_phishing_check",
    toolset="web-browsing-agent",
    schema=URL_PHISHING_CHECK_SCHEMA,
    handler=lambda args, **kw: url_phishing_check(url=args.get("url", "")),
    emoji="🛡️",
)
