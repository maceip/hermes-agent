---
name: cache-storage-management
description: Clear browser cache, manage cookies, localStorage, sessionStorage, service workers, and site permissions
version: 1.0.0
author: Web Browsing Agent
metadata:
  hermes:
    tags: [Web Browsing, Cache, Cookies, Storage, localStorage, Service Workers, Permissions]
    requires_toolsets: [web-browsing-agent]
---

# Cache & Storage Management

## Browser Settings Pages

### Navigating to browser settings:
- Chrome: `chrome://settings/clearBrowserData`
- Firefox: `about:preferences#privacy`
- Edge: `edge://settings/clearBrowserData`

Note: agent-browser uses Chromium — `chrome://settings` paths apply.

## Site-Specific Storage (via browser_console)

### Inspect current site storage:

```javascript
// Show localStorage contents
JSON.stringify(Object.fromEntries(Object.entries(localStorage)), null, 2);
```

```javascript
// Show sessionStorage contents
JSON.stringify(Object.fromEntries(Object.entries(sessionStorage)), null, 2);
```

```javascript
// Show all cookies for current domain
document.cookie;
```

```javascript
// Show IndexedDB databases
(async () => { const dbs = await indexedDB.databases(); return JSON.stringify(dbs); })();
```

### Clear site-specific storage:

```javascript
// Clear localStorage for current site
localStorage.clear();
'localStorage cleared';
```

```javascript
// Clear sessionStorage for current site
sessionStorage.clear();
'sessionStorage cleared';
```

```javascript
// Delete all cookies for current domain
document.cookie.split(";").forEach(c => {
    const name = c.split("=")[0].trim();
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
});
'Cookies cleared for current domain';
```

```javascript
// Delete specific cookie by name
const cookieName = 'COOKIE_NAME_HERE';
document.cookie = cookieName + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
`Cookie '${cookieName}' deleted`;
```

```javascript
// Clear all IndexedDB databases
(async () => {
    const dbs = await indexedDB.databases();
    for (const db of dbs) {
        indexedDB.deleteDatabase(db.name);
    }
    return `Deleted ${dbs.length} IndexedDB databases`;
})();
```

### Service Worker management:

```javascript
// List registered service workers
(async () => {
    const regs = await navigator.serviceWorker.getRegistrations();
    return JSON.stringify(regs.map(r => ({
        scope: r.scope,
        active: r.active?.scriptURL,
        waiting: r.waiting?.scriptURL,
        installing: r.installing?.scriptURL
    })));
})();
```

```javascript
// Unregister all service workers
(async () => {
    const regs = await navigator.serviceWorker.getRegistrations();
    const results = await Promise.all(regs.map(r => r.unregister()));
    return `Unregistered ${results.filter(Boolean).length} service workers`;
})();
```

### Cache API (used by service workers):

```javascript
// List cache storage names
(async () => {
    const names = await caches.keys();
    return JSON.stringify(names);
})();
```

```javascript
// Delete all caches
(async () => {
    const names = await caches.keys();
    await Promise.all(names.map(n => caches.delete(n)));
    return `Deleted ${names.length} caches`;
})();
```

## Storage Quota Information

```javascript
// Check storage usage
(async () => {
    if (navigator.storage && navigator.storage.estimate) {
        const est = await navigator.storage.estimate();
        return JSON.stringify({
            usage_mb: (est.usage / 1024 / 1024).toFixed(2),
            quota_mb: (est.quota / 1024 / 1024).toFixed(2),
            percent_used: ((est.usage / est.quota) * 100).toFixed(1) + '%'
        });
    }
    return 'Storage API not available';
})();
```

## Permission Management

### Check site permissions:

```javascript
// Check common permissions
(async () => {
    const perms = ['geolocation', 'notifications', 'camera', 'microphone', 'clipboard-read', 'clipboard-write'];
    const results = {};
    for (const name of perms) {
        try {
            const p = await navigator.permissions.query({ name });
            results[name] = p.state; // "granted", "denied", "prompt"
        } catch { results[name] = 'not supported'; }
    }
    return JSON.stringify(results, null, 2);
})();
```

### Revoke permissions:
Permissions can only be changed through browser settings, not via JavaScript.
Navigate the user to `chrome://settings/content/siteDetails?site=[url]`.

## Procedures

### Full site reset:
When a user wants to completely reset a site's data:

```
1. Navigate to the site
2. Run all clear commands via browser_console:
   - localStorage.clear()
   - sessionStorage.clear()
   - Delete cookies
   - Delete IndexedDB
   - Unregister service workers
   - Delete caches
3. browser_snapshot → verify the page reloads to a fresh state
4. Report what was cleared
```

### Debugging storage issues:
When a site is behaving incorrectly due to stale data:

```
1. Inspect localStorage for relevant keys
2. Inspect cookies for session/auth tokens
3. Check service workers for stale cached responses
4. Selectively clear the relevant storage
5. Reload the page
6. Verify the issue is resolved
```

### Cookie consent reset:
To re-trigger cookie consent dialogs (change privacy preferences):

```
1. Look for cookies containing "consent", "gdpr", "cookiebot", "onetrust"
2. Delete those specific cookies
3. Reload the page
4. The consent banner should reappear
```
