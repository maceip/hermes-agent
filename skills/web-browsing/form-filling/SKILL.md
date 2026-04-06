---
name: form-filling
description: Navigate and fill web forms including registration, checkout, address entry, and multi-step wizards
version: 1.0.0
author: Web Browsing Agent
metadata:
  hermes:
    tags: [Web Browsing, Forms, Registration, Checkout, Input, Select, Wizard]
    requires_toolsets: [web-browsing-agent]
---

# Form Filling & Web Forms

## Security Boundaries

**You MAY type** (non-sensitive data the user explicitly provides):
- Name, display name, username
- Email address (when user provides it)
- Physical address, city, state, zip
- Phone number (when user provides it)
- Date of birth, preferences
- Search queries, comments, messages

**You MUST NOT type** (always let user type directly):
- Passwords (current, new, or confirmation)
- Credit card numbers, CVV, expiration
- Social Security Numbers or government IDs
- Bank account numbers
- Security answers
- 2FA/MFA codes
- Recovery codes
- API keys or tokens

## Form Field Types

### Text inputs:
```
1. browser_snapshot → find the input field ref
2. browser_click → the ref to focus the field
3. browser_type → enter the text
4. browser_snapshot → verify text was entered correctly
```

### Dropdowns / Select menus:
```
1. browser_snapshot → find the select element
2. browser_click → open the dropdown
3. browser_snapshot → read available options
4. browser_click → the desired option
5. browser_snapshot → verify selection
```

### Radio buttons / checkboxes:
```
1. browser_snapshot → find the option refs
2. browser_click → the desired radio button or checkbox
3. browser_snapshot → verify selection state
```

### Date pickers:
- Some use native date input (type="date") — type in YYYY-MM-DD format
- Some use custom calendar widgets:
  ```
  1. browser_click → the date field to open calendar
  2. browser_snapshot → read the calendar UI
  3. Navigate months if needed (click prev/next arrows)
  4. browser_click → the target date
  ```

### File inputs:
- See file-management skill for details
- Guide user through native file picker dialog

### Rich text editors (TinyMCE, CKEditor, Quill):
```
1. browser_snapshot → find the editor area
2. browser_click → the editor body to focus
3. browser_type → enter text
4. For formatting: use the toolbar buttons (bold, italic, etc.)
```

### CAPTCHAs:
- **reCAPTCHA v2** (checkbox): browser_click the checkbox. If image challenge appears, describe it to user
- **reCAPTCHA v3** (invisible): runs automatically, no interaction needed
- **hCaptcha**: Similar to reCAPTCHA v2 — click checkbox, solve if challenged
- **Image CAPTCHAs**: Use browser_vision to describe the challenge, let user solve
- **Audio CAPTCHAs**: Note the audio option, let user solve

## Multi-Step Forms / Wizards

### Strategy:
```
1. browser_snapshot → identify current step and total steps
2. Read step indicator (Step 1 of 4, progress bar, breadcrumbs)
3. Fill current step fields
4. Click "Next" / "Continue"
5. browser_snapshot → verify moved to next step
6. Repeat until final step
7. On final step → review summary if available
8. Click "Submit" / "Complete" only when user confirms
```

### Handling step errors:
- If "Next" fails → browser_snapshot for error messages
- Scroll up if errors shown at top of form
- Report required fields that were missed
- Fix errors and retry

## Registration Forms

### Typical flow:
```
1. Navigate to sign-up / registration page
2. url_phishing_check → verify legitimate domain
3. browser_snapshot → identify all required fields
4. Fill non-sensitive fields (name, email as provided by user)
5. For password field → tell user to type it directly
6. Handle email verification if required
7. Solve CAPTCHA if present
8. Click "Create Account" / "Sign Up"
9. browser_snapshot → verify success or handle errors
```

### Username availability:
- Many sites check availability in real-time
- After typing username, wait a moment
- browser_snapshot → look for "available" / "taken" indicator

## Checkout Forms

### Typical flow:
```
1. Verify we're on the legitimate checkout page (url_phishing_check)
2. browser_snapshot → identify checkout steps
3. Shipping address: fill with user-provided address
4. Shipping method: describe options, let user choose
5. Payment: STOP — tell user "Please enter your payment details directly"
6. Review order: browser_snapshot → read summary for user
7. Place order: only when user explicitly confirms
```

### Address autocomplete:
```
1. Start typing address
2. browser_snapshot → check for autocomplete dropdown
3. If suggestions appear → read them to user
4. browser_click → correct suggestion, or continue typing
```

## Procedure: Fill Any Form

```
1. browser_snapshot → catalog all form fields
2. Classify each field as sensitive vs non-sensitive
3. For non-sensitive fields:
   a. browser_click the field
   b. browser_type the value
   c. Move to next field
4. For sensitive fields:
   a. Describe the field location to user
   b. Wait for user to fill it
5. browser_snapshot → verify all fields filled
6. Look for validation errors
7. Fix any errors
8. Describe the submit button
9. Click submit when user confirms
10. browser_snapshot → verify success
```
