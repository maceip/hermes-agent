---
name: account-navigation
description: Navigate to account pages, settings panels, profile sections, billing, and subscription management on any website
version: 1.0.0
author: Web Browsing Agent
metadata:
  hermes:
    tags: [Web Browsing, Account, Settings, Navigation, Profile, Billing]
    requires_toolsets: [web-browsing-agent]
---

# Account Page Navigation

Procedures for finding and navigating to account-related pages on any website.

## Discovery Strategy

When asked to find account/settings pages on an unfamiliar site:

1. **Take a snapshot** of the current page to understand the layout
2. **Look for common entry points** in the accessibility tree:
   - User avatar or profile icon (usually top-right)
   - Hamburger menu / three-dot menu
   - "Settings", "Account", "Profile" text links
   - Gear icon or cog icon
   - User email or username displayed in header/nav
3. **Try common URL patterns** if UI elements aren't visible:
   - `/account`, `/settings`, `/profile`, `/preferences`
   - `/dashboard`, `/my-account`, `/user/settings`
   - `/security`, `/privacy`, `/billing`
4. **Fall back to web search** if the above fail:
   - Search: `[site name] account settings URL`
   - Search: `[site name] how to change settings`

## Common Site Patterns

### Google (accounts.google.com)
- Main settings: `https://myaccount.google.com/`
- Security: `https://myaccount.google.com/security`
- Privacy: `https://myaccount.google.com/privacy`
- Data & personalization: `https://myaccount.google.com/data-and-privacy`
- Payments: `https://pay.google.com/`

### Microsoft (account.microsoft.com)
- Main: `https://account.microsoft.com/`
- Security: `https://account.microsoft.com/security`
- Privacy: `https://account.microsoft.com/privacy`
- Devices: `https://account.microsoft.com/devices`

### Apple (appleid.apple.com)
- Main: `https://appleid.apple.com/`
- Sign-in & Security: navigate via main page
- Payment & Shipping: navigate via main page

### Amazon
- Account: `https://www.amazon.com/gp/css/homepage.html`
- Security: Login & Security section within account page
- Addresses: `https://www.amazon.com/a/addresses`

### GitHub
- Settings: `https://github.com/settings/profile`
- Security: `https://github.com/settings/security`
- SSH keys: `https://github.com/settings/keys`
- Applications: `https://github.com/settings/applications`

## Navigation Procedure

```
1. browser_navigate → site URL
2. browser_snapshot → read page structure
3. Identify settings/account link in accessibility tree
4. browser_click → the link reference
5. browser_snapshot → verify we reached the settings page
6. If login required → guide user (never enter credentials)
7. Report page structure and available options to user
```

## Handling Login Walls

Many settings pages require authentication:

1. **Detect login page**: Look for password fields, "Sign in" buttons
2. **Run phishing check**: url_phishing_check on the current URL
3. **Report to user**: "This page requires login. I can see the username and password fields. Please enter your credentials — I will not type them for you."
4. **Wait for user confirmation** before proceeding
5. **After login**: Take new snapshot and continue navigation

## Settings Page Categories

When on a settings page, help the user find the right section:

| Category | Common labels |
|----------|--------------|
| Profile | Profile, Personal info, Display name, Bio, Avatar |
| Security | Security, Password, 2FA, Login activity, Sessions |
| Privacy | Privacy, Data, Visibility, Who can see |
| Notifications | Notifications, Alerts, Email preferences |
| Billing | Billing, Payments, Subscription, Plan |
| Connected apps | Connected apps, Integrations, OAuth, Third-party |
| Language/Region | Language, Region, Timezone, Locale |
| Accessibility | Accessibility, Display, Appearance, Theme |
| Data export | Download data, Export, Your data, GDPR |
| Delete account | Delete account, Close account, Deactivate |
