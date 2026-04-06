---
name: popup-cookie-handling
description: Dismiss cookie banners, notification prompts, consent dialogs, modal overlays, and GDPR pop-ups on websites
version: 1.0.0
author: Web Browsing Agent
metadata:
  hermes:
    tags: [Web Browsing, Cookies, Pop-ups, Consent, GDPR, Modals, Overlays, Banners]
    requires_toolsets: [web-browsing-agent]
---

# Pop-up & Cookie Handling

## General Strategy

```
1. browser_snapshot → identify overlay type
2. Classify: cookie consent | notification prompt | modal | paywall | newsletter | chat widget
3. Find dismiss button (Reject All > X close > Deny > Dismiss)
4. browser_click → dismiss element
5. browser_snapshot → verify overlay is gone
6. If persistent → use browser_console to remove element
```

## Cookie Consent Banners (GDPR/CCPA)

### Common patterns:

**Banner at bottom/top of page:**
- Look for: "Accept", "Reject All", "Manage Preferences", "Cookie Settings"
- **Preferred action**: Click "Reject All" or "Necessary Only" (minimal tracking)
- If only "Accept All" exists: look for "Manage" → then deselect optional cookies

**Full-screen overlay:**
- Blocks page interaction until resolved
- Look for: "Reject", "Decline", "Continue without accepting"
- Sometimes hidden behind "More Options" or "Manage Settings"

**Consent management platforms (CMPs):**
| CMP | Identifier | Strategy |
|-----|-----------|----------|
| OneTrust | `#onetrust-banner-sdk` | Click "Reject All" button |
| Cookiebot | `.CybotCookiebotDialog` | Click "Deny" or "Only necessary" |
| TrustArc | `#truste-consent-track` | Click "Decline All" or close button |
| Quantcast | `.qc-cmp2-container` | Click "DISAGREE" or "Manage options" → reject |
| Didomi | `#didomi-notice` | Click "Disagree" or "Refuse" |
| Generic | Various | Look for ref with "reject", "decline", "deny", "necessary only" text |

### JavaScript fallback:
If the banner persists after clicking, use browser_console:

```javascript
// Remove common cookie banner containers
document.querySelectorAll('[class*="cookie"], [id*="cookie"], [class*="consent"], [id*="consent"], [class*="gdpr"]').forEach(el => el.remove());

// Remove overlay/backdrop
document.querySelectorAll('[class*="overlay"], [class*="backdrop"], [class*="modal-backdrop"]').forEach(el => el.remove());

// Restore body scrolling
document.body.style.overflow = 'auto';
document.documentElement.style.overflow = 'auto';
```

## Notification Permission Prompts

### Browser-level prompts:
- These appear as browser-native dialogs, not page elements
- **Cannot be dismissed via browser_click** (not in accessibility tree)
- Use browser_press with "Escape" key, or browser_console:

```javascript
// Block notification requests
if (window.Notification) {
    window.Notification.requestPermission = () => Promise.resolve('denied');
}
```

### In-page notification prompts:
- "Enable notifications to stay updated"
- "Allow push notifications"
- Look for "No thanks", "Not now", "Maybe later", X button
- Click the dismiss option

## Modal Overlays

### Newsletter / signup modals:
- "Subscribe to our newsletter"
- "Sign up for 10% off"
- Look for: X close button (usually top-right of modal), "No thanks", "Close"
- Check accessibility tree for `dialog` role or `aria-modal="true"`

### Paywall modals:
- "Subscribe to continue reading"
- "You've reached your free article limit"
- Options:
  1. Click X or close if available
  2. Try browser_console: `document.querySelector('[class*="paywall"], [class*="gate"]')?.remove(); document.body.style.overflow='auto';`
  3. Inform user about the paywall and subscription options

### Age verification gates:
- "Are you 18+?" / "Confirm your age"
- Look for "Yes, I am" or birth year entry
- **Let user decide** — do not auto-confirm age

### Location permission dialogs:
- In-page: look for "Deny" or "Block" option
- Browser-level: use Escape key

## Chat Widgets

### Floating chat buttons (Intercom, Drift, Zendesk, etc.):
- Usually bottom-right corner
- Rarely block interaction but can obscure content
- Remove if needed:

```javascript
// Common chat widget selectors
document.querySelectorAll('#intercom-container, .intercom-lightweight-app, [class*="drift-"], #hubspot-messages-iframe-container, #launcher, .zEWidget-launcher, [class*="crisp-"], #tidio-chat').forEach(el => el.remove());
```

## Social Media Overlays

### "Login to continue" prompts (Pinterest, LinkedIn, Quora):
- Often triggered after scrolling
- Look for X close or "Continue browsing"
- JavaScript fallback:

```javascript
// Remove login walls
document.querySelectorAll('[class*="login-wall"], [class*="signup-modal"], [class*="auth-modal"], [role="dialog"]').forEach(el => el.remove());
document.body.style.overflow = 'auto';
document.body.classList.remove('no-scroll', 'modal-open', 'overflow-hidden');
```

### App download banners:
- "Get the app" / "Open in app" banners on mobile-formatted pages
- Look for X close or "Continue in browser"
- Usually a top banner element

## Procedure Checklist

For any new pop-up encountered:

- [ ] Snapshot the page
- [ ] Identify the overlay type
- [ ] Look for the least-intrusive dismiss option (Reject > Close > Escape)
- [ ] Click dismiss
- [ ] Snapshot again to verify removal
- [ ] If still present, try JavaScript removal via browser_console
- [ ] If still blocking, report to user with options
- [ ] Check if body scroll was restored
