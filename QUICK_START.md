# Quick Start Guide - Theater Infotainment System

## 🚀 Get Started in 3 Steps

### Step 1: Populate Database
```bash
python populate_db.py
```
This creates 5 opera events with multiple performances scheduled for this month.

### Step 2: Start Server
```bash
python manage.py runserver
```

### Step 3: Test the App
- **Admin Panel**: http://localhost:8000/admin/
- **English Home**: http://localhost:8000/home/
- **Arabic Home**: http://localhost:8000/home_ar/

---

## 📋 What's Been Created

### Events (10 operas):
1. La Traviata - Verdi
2. Carmen - Bizet
3. The Magic Flute - Mozart
4. Rigoletto - Verdi
5. Tosca - Puccini
6. Aida - Verdi
7. Don Giovanni - Mozart
8. La Bohème - Puccini
9. The Barber of Seville - Rossini
10. Madama Butterfly - Puccini

### Performances:
- 4-6 shows per event (50+ total)
- **Tighter schedule** with events every 3-4 days
- **Multiple events on same days**
- Times: 2:00 PM, 3:00 PM, 5:30 PM, 6:00 PM, 7:00 PM, 7:30 PM

---

## 🎯 Key Admin Features

### Manage Events
**Location**: Admin > Theater CMS > Events

**What you can do**:
- View all events
- Edit event details (title, composer, cast, etc.)
- Add event images
- Add Arabic translations
- Set active/inactive status

### Schedule Performances
**Location**: Admin > Theater CMS > Performances

**What you can do**:
- View calendar-style performance list
- Schedule new performances
- Filter by event or date
- Duplicate performances quickly
- See multiple events on same day

**Features**:
- 📅 Calendar date display
- 🕐 Time slots with duration
- 🎭 Color-coded events
- ➕ Quick duplicate button
- 🔍 Search by event name (English/Arabic)

---

## 🌐 Test Both Languages

### English Pages:
- `/home/` - Home page
- `/events/` - Events list
- `/event/<slug>/` - Event detail
- `/greetings/` - Greeting page
- `/sponsors/` - Sponsors page

### Arabic Pages (same structure):
- `/home_ar/`
- `/events_ar/`
- `/event_ar/<slug>/`
- `/greetings_ar/`
- `/sponsors_ar/`

---

## ✅ Testing Checklist

### Basic Functionality:
- [ ] Events display on home page
- [ ] Can browse all events
- [ ] Event details show correctly
- [ ] Arabic translations work
- [ ] Performance calendar displays

### Admin Panel:
- [ ] Can view events list
- [ ] Can edit event details
- [ ] Can add new performances
- [ ] Can filter performances by event
- [ ] Can search events
- [ ] Date hierarchy works

### Scheduling System:
- [ ] Can schedule multiple events on same day
- [ ] Can duplicate performances
- [ ] Calendar view shows all performances
- [ ] Filters work correctly
- [ ] Search finds events

---

## 🎨 Adding Images

### Event Images:
1. Go to Admin > Events
2. Click on an event
3. Scroll to "Image" field
4. Upload image
5. Save

### Sponsor Images:
1. Go to Admin > Seasonal Sponsors or Event Sponsor Images
2. Click "Add" or edit existing
3. Upload image
4. Save

---

## 🔧 Common Commands

### Database:
```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate test data
python populate_db.py
```

### Development:
```bash
# Run server
python manage.py runserver

# Check for issues
python manage.py check

# Collect static files
python manage.py collectstatic
```

---

## 📱 Target Platform

- **Device**: Android 6.0 tablets
- **Resolution**: 1024x600 pixels
- **Browser**: WebView (older version)
- **Features**: Touch-optimized, fixed viewport

---

## 💡 Tips

1. **No Images Initially**: The populate script doesn't include images. Add them manually through admin.

2. **Current Month**: Performances are scheduled for the current month. Re-run the script next month to update.

3. **Multiple Events Same Day**: Test scheduling Rigoletto at 3 PM and Carmen at 6 PM on the same day.

4. **Arabic Testing**: Make sure to test both English and Arabic versions to verify translations.

5. **Performance Calendar**: The new unified calendar interface makes it easy to see all scheduled performances at a glance.

---

## 🆘 Need Help?

- Check `POPULATE_DB_README.md` for detailed documentation
- Review `plan.md` for system architecture
- Check console for error messages
- Verify all migrations are applied

---

**Ready to test! 🎭🎉**

