---
name: password-passkey-management
description: Navigate password change flows, set up passkeys/WebAuthn, manage 2FA/MFA, and handle recovery options on websites
version: 1.0.0
author: Web Browsing Agent
metadata:
  hermes:
    tags: [Web Browsing, Password, Passkey, WebAuthn, 2FA, MFA, Security, FIDO2]
    requires_toolsets: [web-browsing-agent]
---

# Password & Passkey Management

## Critical Security Rules

1. **NEVER type passwords** — navigate to the field, describe it, let the user type
2. **NEVER type recovery codes** — show the user where to enter them
3. **ALWAYS run url_phishing_check** before any page with credential fields
4. **Verify the domain** before telling the user it's safe to enter credentials
5. **Screenshot sensitive pages** using browser_vision for spatial verification

## Password Change Flow

### Step-by-step procedure:

```
1. Navigate to the site's security/password settings
2. browser_snapshot → find "Change password" or "Update password" link/button
3. browser_click → the change password element
4. browser_snapshot → identify form fields:
   - Current password field (describe its ref to user)
   - New password field
   - Confirm password field
5. Tell user: "I found the password change form. The fields are:
   - Current password: [describe field location]
   - New password: [describe field]
   - Confirm: [describe field]
   Please type your current password, then your new password."
6. After user types → browser_snapshot to verify fields populated
7. Find and click Submit/Save button
8. browser_snapshot → verify success or handle errors
```

### Common password page paths:
- `/settings/security`
- `/account/password`
- `/settings/password`
- `/security/password-change`
- `/profile/security`

### Error handling:
- "Password too weak" → report requirements to user
- "Current password incorrect" → tell user to re-enter
- "Passwords don't match" → tell user to re-enter new password
- Session expired → guide user through re-authentication

## Passkey / WebAuthn Setup

### What are passkeys?
Passkeys replace passwords with biometric/device-based authentication (FIDO2/WebAuthn). They use public-key cryptography — the private key never leaves the device.

### Setting up a passkey:

```
1. Navigate to security settings
2. browser_snapshot → look for:
   - "Passkey", "Passkeys"
   - "Security Key"
   - "WebAuthn"
   - "Passwordless"
   - "FIDO2"
   - "Biometric login"
3. browser_click → the passkey setup option
4. browser_snapshot → read setup instructions
5. Tell user: "The site is ready to register a passkey. 
   When you click the button, your browser/device will prompt you 
   to authenticate (fingerprint, face, or PIN). I cannot interact 
   with that system dialog — you'll need to complete it yourself."
6. browser_click → "Add passkey" / "Register" button
7. Wait for user to complete device authentication
8. browser_snapshot → verify registration succeeded
```

### Common passkey support pages:
| Site | Path |
|------|------|
| Google | myaccount.google.com → Security → Passkeys |
| Apple | appleid.apple.com → Sign-In and Security → Passkeys |
| Microsoft | account.microsoft.com → Security → Advanced security → Passkeys |
| GitHub | github.com/settings/security → Passkeys |
| PayPal | paypal.com → Settings → Security → Passkeys |

## 2FA / MFA Management

### Types of 2FA:
1. **TOTP (authenticator app)** — Google Authenticator, Authy, 1Password
2. **SMS codes** — phone number verification
3. **Hardware keys** — YubiKey, Titan Security Key
4. **Backup codes** — one-time recovery codes
5. **Email codes** — sent to recovery email

### Setting up TOTP:

```
1. Navigate to 2FA/MFA settings
2. browser_snapshot → find "Two-factor" or "2FA" or "Multi-factor" option
3. browser_click → enable 2FA
4. browser_snapshot → look for QR code or setup key
5. If QR code visible:
   - Use browser_get_images to extract QR code image
   - Tell user: "I can see the QR code. Scan it with your authenticator app."
   - Or use browser_vision to read the setup key text
6. If text key shown:
   - Read the key from snapshot
   - Tell user: "Manual setup key: [key]. Enter this in your authenticator app."
7. The site will ask for a verification code:
   - Tell user: "Enter the 6-digit code from your authenticator app"
   - Point to the input field reference
8. browser_snapshot → verify success
9. IMPORTANT: Look for backup/recovery codes
   - Tell user: "Save these recovery codes somewhere safe — 
     they're your backup if you lose your authenticator."
```

### Disabling 2FA:
- Usually requires current 2FA code to confirm
- Some sites require password re-entry
- Warn user about security implications

## Recovery Options

### Setting up recovery:
- **Recovery email**: Navigate to recovery settings, identify email field
- **Recovery phone**: Navigate to phone verification settings
- **Security questions**: Read questions, let user type answers
- **Backup codes**: Download or display, tell user to save them

### Using recovery:
- **Forgot password flow**: Navigate to "Forgot password?" link on login page
- **Recovery code entry**: Navigate to recovery input, describe the field
- **Account recovery form**: Help navigate multi-step recovery process

## Session Management

### Viewing active sessions:
```
1. Navigate to security settings
2. Look for "Active sessions", "Where you're logged in", "Devices"
3. browser_snapshot → list all sessions with details
4. Report: device type, location, last activity, IP
5. If user wants to sign out a session → click "Sign out" for that entry
```

### Revoking app access:
```
1. Navigate to "Connected apps" or "Third-party apps" or "OAuth"
2. browser_snapshot → list all connected applications
3. Report each app's permissions and last access
4. If user wants to revoke → click "Revoke" or "Remove access"
5. browser_snapshot → confirm revocation
```
