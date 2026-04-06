---
name: file-management
description: Handle file uploads, downloads, file pickers, drag-and-drop zones, and attachment management in web applications
version: 1.0.0
author: Web Browsing Agent
metadata:
  hermes:
    tags: [Web Browsing, Files, Uploads, Downloads, Attachments, File Picker]
    requires_toolsets: [web-browsing-agent]
---

# File Management in Web Applications

## File Upload Patterns

### Standard file input (`<input type="file">`):
```
1. browser_snapshot → find the file input or upload button
2. Identify the element ref (@eN)
3. Tell user: "I found the file upload field. Click it to open your file picker."
   Note: browser_click on file inputs triggers the native OS file dialog 
   which the agent CANNOT interact with — the user must select the file.
4. After user selects file → browser_snapshot to verify file name appears
5. Look for "Upload" / "Submit" button and click if user confirms
```

### Drag-and-drop zones:
- Often styled as dashed-border rectangles with "Drag files here" text
- These also have a hidden file input — look for a "Browse" or "Choose file" fallback link
- Guide user to use the fallback click-to-browse option

### Multi-file uploads:
- Look for "Add more files" or "+" buttons after first upload
- Some sites support selecting multiple files at once (multiple attribute)
- Report maximum file size/count limits if visible on page

### Progress indicators:
```
1. After upload starts → browser_snapshot periodically
2. Look for progress bars, percentage text, or status messages
3. Report progress to user
4. Wait for completion indicator before proceeding
```

## File Download Patterns

### Direct download links:
```
1. browser_snapshot → find download link/button
2. browser_click → the download element
3. Note: In headless browser, downloads go to a default directory
4. Tell user where to find the downloaded file
5. If download doesn't start → check for confirmation dialogs
```

### Export / data download:
- "Export as CSV", "Download PDF", "Export data"
- May trigger a format selection dialog first
- Some exports take time to generate (look for "Preparing download..." messages)

### Bulk downloads:
- Some sites offer "Download all" or zip archives
- Google Takeout, Facebook download — multi-step export processes
- Guide user through the request → wait → download flow

## Cloud File Managers

### Google Drive:
- Navigate: `https://drive.google.com/`
- Upload: "New" button → "File upload" or "Folder upload"
- Share: Right-click file → "Share" → manage permissions
- Move: Drag or right-click → "Move to"

### Dropbox:
- Navigate: `https://www.dropbox.com/home`
- Upload: "Upload" button in top bar
- Share: "Share" button on file hover → enter email/create link

### OneDrive:
- Navigate: `https://onedrive.live.com/`
- Upload: "Upload" dropdown → "Files" or "Folder"
- Share: "Share" button → configure link settings

### iCloud Drive:
- Navigate: `https://www.icloud.com/iclouddrive`
- Upload: Upload button in toolbar
- Share: Select file → share icon

## Attachment Management (Email, Chat, etc.)

### Email attachments:
```
1. In compose view → find "Attach" button (usually paperclip icon)
2. browser_click → triggers file picker
3. Guide user to select file
4. Verify attachment appears in compose area
5. Check for size limit warnings
```

### Chat file sharing (Slack, Teams, Discord):
- Usually a "+" button or paperclip icon near message input
- Drag-and-drop support in the message area
- Preview generation for images/documents
- Size limits vary by platform/plan

## File Preview & Viewing

### In-browser previews:
- PDFs: Most browsers render inline
- Images: Standard browser rendering
- Documents: Google Docs Viewer, Microsoft Office Online
- Videos: HTML5 video player

### Handling "Open with" prompts:
- "Open in Google Docs" / "Open in Microsoft Word Online"
- Let user choose their preferred viewer
- Some files require third-party viewers

## Procedures

### Upload a file to a web app:
```
1. Navigate to the target page/form
2. browser_snapshot → locate upload area
3. Identify if it's an input, drop zone, or button
4. If input/button → browser_click and guide user through file picker
5. If drop zone → find fallback "Browse" link
6. browser_snapshot → verify file selected
7. Click Upload/Submit if present
8. browser_snapshot → confirm success
```

### Download account data (GDPR export):
```
1. Navigate to account settings → Privacy/Data section
2. Look for "Download your data", "Request data export", "Your data"
3. browser_click → start the export
4. Fill in any options (date range, data types)
5. Submit the request
6. Note: exports often take hours/days — the site will email when ready
7. Tell user what to expect (processing time, email notification)
```
