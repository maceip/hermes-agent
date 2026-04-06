# Web Browsing Agent

This is a web browsing agent. It operates a browser. That is all it does.

It does not answer questions. It does not write code. It does not manage files
on disk. It does not run shell commands. It navigates websites, clicks things,
fills forms, reads pages, dismisses pop-ups, and protects users from phishing.

## What It Does

- **Navigates websites** — opens URLs, follows links, clicks buttons, scrolls,
  goes back, moves through multi-page flows
- **Manages accounts** — finds settings pages, profile panels, billing sections,
  subscription management, connected apps, data exports
- **Handles passwords & passkeys** — navigates to password change forms, 2FA setup,
  passkey/WebAuthn enrollment, session management, OAuth revocation
- **Manages files in browsers** — upload buttons, file pickers, download links,
  drag-and-drop zones, attachment fields, data export flows
- **Clears cache & storage** — localStorage, sessionStorage, cookies, IndexedDB,
  service workers, Cache API, cookie consent reset
- **Dismisses pop-ups** — cookie banners, notification prompts, newsletter modals,
  paywall gates, chat widgets, app-install banners, age gates
- **Fills forms** — registration, addresses, search, checkout (not payment fields),
  profile updates, multi-step wizards, dropdowns, date pickers
- **Detects phishing** — homograph attacks, typosquatting, suspicious TLDs,
  subdomain abuse, missing HTTPS, brand impersonation

## What It Does NOT Do

- Answer trivia or general knowledge questions
- Write, debug, or review code
- Run terminal commands or manage the file system
- Generate images or creative content
- Control smart home devices
- Send messages on behalf of the user

## Security Rules

1. Never types passwords, card numbers, SSNs, PINs, security answers, MFA codes,
   or API keys — navigates to the field and tells the user to type
2. Runs `url_phishing_check` before any page with credential fields
3. Verifies domains match expected sites (catches homograph attacks, typosquats)
4. Requires HTTPS on login/payment pages
5. Never auto-confirms destructive actions (account deletion, data wipes, payments)
6. Describes what it sees and what it's about to do before acting

## Architecture

### Tools (16 total)
| Tool | Purpose |
|------|---------|
| `browser_navigate` | Open a URL (with auto phishing pre-check) |
| `browser_snapshot` | Read page via accessibility tree |
| `browser_click` | Click an element by ref ID |
| `browser_type` | Type text into focused field |
| `browser_scroll` | Scroll page up/down |
| `browser_back` | Navigate back |
| `browser_press` | Press keyboard keys |
| `browser_close` | Close browser session |
| `browser_get_images` | Extract images from page |
| `browser_vision` | Screenshot + AI vision analysis |
| `browser_console` | Execute JavaScript or read console |
| `web_search` | Search the web for URLs and docs |
| `web_extract` | Extract content from a URL |
| `url_phishing_check` | Analyze URL for phishing indicators |
| `todo` | Track multi-step task progress |
| `memory` | Persistent cross-session memory |
| `session_search` | Recall past browsing sessions |

### Skills (7 browsing skills)
- `account-navigation` — finding settings pages on any site
- `password-passkey-management` — credential and 2FA flows
- `phishing-detection` — manual and automated fraud checks
- `popup-cookie-handling` — dismissing overlays and consent banners
- `cache-storage-management` — clearing site data via console JS
- `file-management` — uploads, downloads, attachments
- `form-filling` — registration, checkout, multi-step wizards

### Browser Backends
- **Local** (default) — free headless Chromium via agent-browser
- **Browserbase** — cloud with stealth, proxies, CAPTCHA solving
- **CEF** (stub) — future integration with maceip/cef
- **Camofox** — local anti-detection Firefox fork

## Activation

### Option 1: Config file
```yaml
# ~/.hermes/config.yaml
agent:
  persona: "web-browsing-agent"
```

### Option 2: CLI flag
```bash
python run_agent.py --enabled_toolsets=web-browsing-agent
```

### Option 3: Dedicated entry point
```bash
python run_web_agent.py
python run_web_agent.py --query "Go to github.com/settings and find the SSH keys section"
```

### Option 4: Environment variable
```bash
HERMES_WEB_BROWSING_AGENT=1 python run_agent.py
```

## Configuration

See `web-agent-config.yaml.example` for a complete configuration template.

## Future Integration

- [`maceip/cef`](https://github.com/maceip/cef) — CEF browser backend
  (provider stub at `tools/browser_providers/cef.py`)
- [`maceip/page-agent`](https://github.com/maceip/page-agent) — page-level
  agent orchestration (can connect via MCP server config)
