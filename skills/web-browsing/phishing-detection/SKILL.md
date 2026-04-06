---
name: phishing-detection
description: Detect phishing sites, verify domain authenticity, identify fraud indicators, and protect users from credential theft
version: 1.0.0
author: Web Browsing Agent
metadata:
  hermes:
    tags: [Web Browsing, Phishing, Fraud, Security, Homograph, Domain Verification]
    requires_toolsets: [web-browsing-agent]
---

# Phishing & Fraud Detection

## Automated Checks

The `url_phishing_check` tool runs automatically on every navigation via
`browser_navigate` and is also available as a standalone tool. It checks:

- **Homograph attacks**: Cyrillic/Greek characters that look like Latin letters
- **Typosquatting**: Domains 1-2 characters away from known brands
- **Suspicious TLDs**: .tk, .ml, .ga, .cf, .gq, .xyz, .top, .buzz, .icu
- **Subdomain abuse**: Brand names in subdomains of unrelated domains
- **Protocol**: HTTP vs HTTPS on pages that handle credentials

## Manual Verification Checklist

When the automated tool flags something, or when navigating to any login or
payment page, perform these additional checks:

### Domain Verification
```
1. browser_snapshot → read the current URL from page data
2. url_phishing_check → run on the URL
3. Check: Does the domain match what the user expects?
4. Check: Is the TLD correct? (.com vs .co, .org vs .net)
5. Check: Any unusual subdomains? (login-google.evil.com)
6. Report findings clearly to user
```

### Page Content Verification
```
1. browser_snapshot → read page structure
2. Look for red flags:
   - Urgency language: "Your account will be suspended"
   - Unusual requests: "Verify your SSN/credit card"
   - Poor grammar/spelling in official-looking pages
   - Missing or broken images (using browser_get_images)
   - Login form on a non-standard page
3. browser_vision → take screenshot for visual verification:
   - Logo quality (blurry, wrong colors)
   - Layout inconsistencies
   - Missing footer links (privacy policy, terms)
4. Report what looks legitimate vs suspicious
```

### Certificate & Connection
```
1. Check URL starts with https://
2. Look for mixed content warnings in browser_console
3. If HTTP on a login page → CRITICAL warning to user
4. If redirect chain detected (URL changed) → verify final domain
```

## Common Phishing Patterns

### Credential Harvesting
- Fake login pages that look identical to real ones
- Email links to "verify your account"
- "Your password expired" alerts
- "Unusual sign-in detected" notifications

**How to spot:**
- URL domain doesn't match the real service
- Page loaded from an email link rather than direct navigation
- Multiple redirects before landing
- Login page asks for information the real site doesn't

### OAuth Phishing
- Fake "Sign in with Google/Microsoft" buttons
- Malicious OAuth apps requesting excessive permissions
- Redirect URI manipulation

**How to spot:**
- OAuth consent screen domain is not accounts.google.com (or equivalent)
- App requests permissions beyond what's needed
- Unknown developer name in consent screen

### Payment Fraud
- Fake checkout pages
- Modified payment forms injecting additional fields
- Card skimming overlays on legitimate sites

**How to spot:**
- Checkout URL doesn't match the shopping site
- Extra fields (SSN, PIN, mother's maiden name)
- Payment form not embedded via iframe from known processor

### Browser Extension Phishing
- Fake extension permission dialogs
- Extensions requesting excessive permissions
- Mimicking Chrome Web Store pages

**How to spot:**
- Permission dialog appears outside normal install flow
- Extension source URL is not chrome.google.com/webstore
- Requests "Read and change all your data on all websites"

## Response Procedures

### When risk_level is "critical":
```
1. IMMEDIATELY warn user: "CRITICAL: This appears to be a phishing site."
2. Explain specific findings
3. Recommend: "Do NOT enter any credentials or personal information."
4. Suggest: "Navigate to [service] directly by typing the URL manually."
5. Do NOT interact with any form fields
```

### When risk_level is "high":
```
1. Warn user with specific findings
2. Ask user to verify: "Is this the site you intended to visit?"
3. Suggest verifying via bookmark or manual URL entry
4. Do not interact with credential fields until user confirms
```

### When risk_level is "medium":
```
1. Note the findings to user
2. Suggest extra verification before entering sensitive data
3. Proceed with caution if user confirms
```

### When risk_level is "low":
```
1. Proceed normally
2. Still verify domain matches expectations before credentials
3. Standard browsing caution applies
```

## Reporting Phishing

If a phishing site is confirmed, guide the user to report it:
- **Google Safe Browsing**: https://safebrowsing.google.com/safebrowsing/report_phish/
- **Microsoft**: https://www.microsoft.com/en-us/wdsi/support/report-unsafe-site
- **Anti-Phishing Working Group**: reportphishing@apwg.org
- **Browser built-in**: Most browsers have "Report unsafe site" in menu
