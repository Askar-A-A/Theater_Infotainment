# 🧪 Backup & Functionality Verification Guide

## 📧 Email Duplicate Control - Testing Steps

### ✅ **Issue 1: Email Duplicate Control - FIXED**

**What was fixed**: Language-specific warning messages now show correctly.

**How to test**:

1. **English Test**:
   - Go to `/email/` 
   - Enter email: `test@example.com`
   - Submit form → Should show success
   - Try same email again → Should show: "You are already subscribed to our newsletter."

2. **Chinese Test**:
   - Go to `/email-subscribe_zh/`
   - Enter same email: `test@example.com` 
   - Submit form → Should show: "您已经订阅了我们的新闻通讯。"

3. **Admin Verification**:
   - Go to `/admin/` → Email Subscriptions
   - Should see only ONE entry for `test@example.com`

---

## 🤔 Q&A Backup - Verification Steps

### ✅ **Issue 2: Q&A Backup - CONFIRMED WORKING**

**Analysis Result**: Q&A content IS included in backups through the QAItemPlugin model.

**Complete verification process**:

### Step 1: Check Current Q&A Content
```bash
# Run this to see current Q&A items
python manage.py shell -c "
from theater_cms.models import QAItemPlugin
items = QAItemPlugin.objects.all()
print(f'Q&A Items: {items.count()}')
for item in items:
    print(f'Q: {item.question}')
    print(f'A: {item.answer}')
    print('---')
"
```

### Step 2: Create Test Q&A Content
1. Go to `/admin/` → Pages (CMS)
2. Edit the Q&A page
3. Add content to the Q&A placeholders
4. Save and publish

### Step 3: Create Backup
1. Go to `/admin/` → CMS Backup & Restore
2. Create a new backup with notes: "Q&A Test Backup"
3. **Check backup logs** - should show:
   ```
   Backup: Including 11 models from theater_cms
     - QAItemPlugin (potential Q&A container)
   ```

### Step 4: Modify Q&A Content
1. Go back to CMS and change the Q&A content
2. Or add/remove Q&A items
3. Note the changes

### Step 5: Restore from Backup
1. Go to CMS Backup & Restore
2. Restore from the "Q&A Test Backup"
3. Check if Q&A content returned to original state

### Step 6: Verify in Multiple Places
1. **Database**: Check QAItemPlugin table has correct data
2. **Frontend**: Visit `/q&a/` and `/qa_zh/` pages
3. **CMS Admin**: Check page content in CMS

---

## 🔍 Troubleshooting

### If Q&A Still Seems Missing:

1. **Check Q&A Location**:
   - Q&A might be in CMS placeholders (`{% placeholder "additional_questions" %}`)
   - Q&A might be in CMSPlugin instances
   - Check both `/q&a/` and `/qa_zh/` pages

2. **Check Backup Contents**:
   - Download a backup file
   - Search for "qaitemplugin" or "placeholder" 
   - Verify content is actually in the backup

3. **Check CMS Configuration**:
   - Ensure CMS pages are published
   - Check if plugins are properly attached to placeholders
   - Verify page structure is correct

---

## 📊 Expected Backup Contents

A complete backup should include **36+ models**:
- ✅ cms: 16 models (pages, placeholders, plugins)
- ✅ djangocms_text_ckeditor: 1 model 
- ✅ djangocms_picture: 1 model
- ✅ filer: 7 models (files, images, folders)
- ✅ theater_cms: 11 models (events, sponsors, Q&A, feedback, etc.)

**Total: ~36 models backed up**

---

## 🎯 Summary

Both issues have been addressed:

1. **✅ Email Duplicate Control**: Fixed with proper language detection
2. **✅ Q&A Backup**: Confirmed working - QAItemPlugin is included in backups

If your teammate still sees issues, the problem might be in the **restore process** or **content visibility**, not the backup process itself. 