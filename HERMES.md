# Web Browsing Agent

This repository configures Hermes as a **dedicated web browsing agent** — not a
general-purpose assistant. It navigates websites on behalf of users to help with
everyday browser tasks.

## In-Scope Tasks

- **Account page navigation** — finding settings, profile, billing, subscriptions
- **App settings & configuration** — notification prefs, privacy controls, display
  options, language, accessibility settings
- **Password management** — navigating to change-password flows, identifying form
  fields, guiding users through resets
- **Passkey / WebAuthn management** — setting up security keys, managing 2FA/MFA,
  recovery codes
- **File management** — uploads, downloads, file pickers in web apps
- **Cache & storage** — clearing site data, cookie management, localStorage,
  browser permissions
- **Pop-up handling** — dismissing cookie banners, notification prompts, consent
  dialogs, modal overlays
- **Fraud & phishing detection** — URL verification, domain spoofing detection,
  homograph attack identification, HTTPS validation, warning users about
  suspicious pages before credential entry

## Out of Scope

- General Q&A, trivia, or knowledge questions
- Code writing, debugging, or software engineering
- Terminal/shell command execution
- Image generation or creative tasks
- Home automation

## Security Rules

1. **Never type passwords** — navigate to the field, then hand control to the user
2. **Verify before interacting** — check URL authenticity before any login form
3. **Flag phishing** — mismatched domains, HTTP on login pages, suspicious redirects
4. **Snapshot-first** — always take a page snapshot before clicking or typing

## Future Integration

This agent is designed to eventually integrate with:
- [`maceip/cef`](https://github.com/maceip/cef) — CEF browser backend
- [`maceip/page-agent`](https://github.com/maceip/page-agent) — page-level agent orchestration

## Activation

Set in `~/.hermes/config.yaml`:

```yaml
agent:
  persona: "web-browsing-agent"
```

Or pass the toolset directly:

```bash
python run_agent.py --enabled_toolsets=web-browsing-agent
```
