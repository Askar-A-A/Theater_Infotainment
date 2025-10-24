# Database Population Script

This script populates the Theater Infotainment database with sample opera events and performances for testing purposes.

## What It Creates

### 🎭 10 Popular Opera Events:
1. **La Traviata** by Giuseppe Verdi
2. **Carmen** by Georges Bizet
3. **The Magic Flute** by Wolfgang Amadeus Mozart
4. **Rigoletto** by Giuseppe Verdi
5. **Tosca** by Giacomo Puccini
6. **Aida** by Giuseppe Verdi
7. **Don Giovanni** by Wolfgang Amadeus Mozart
8. **La Bohème** by Giacomo Puccini
9. **The Barber of Seville** by Gioachino Rossini
10. **Madama Butterfly** by Giacomo Puccini

### 📅 Performances:
- 4-6 performances per event (50+ total performances)
- **Tighter scheduling** with performances every 3-4 days
- **Multiple events on same days** (e.g., Rigoletto at 3 PM, Aida at 6 PM)
- Various times: 2:00 PM, 3:00 PM, 5:30 PM, 6:00 PM, 7:00 PM, 7:30 PM
- Each performance is 3 hours long

### 🌐 Bilingual Content:
- All events include both English and Arabic translations
- Titles, composer names, descriptions, cast lists
- Ready to test both language versions of the app

## Usage

### Run the Script:
```bash
python populate_db.py
```

### What It Does:
1. ✅ Clears existing events and performances (fresh start)
2. ✅ Creates 10 opera events with full details
3. ✅ Schedules 50+ performances with tight scheduling
4. ✅ Creates multiple events on same days
5. ✅ Displays a summary with multi-event days highlighted

### Expected Output:
```
🗑️  Clearing existing data...
✅ Existing data cleared

🎭 Creating opera events...
  ✅ Created: La Traviata (لا ترافياتا)
  ✅ Created: Carmen (كارمن)
  ✅ Created: The Magic Flute (الناي السحري)
  ✅ Created: Rigoletto (ريجوليتو)
  ✅ Created: Tosca (توسكا)
  ✅ Created: Aida (عايدة)
  ✅ Created: Don Giovanni (دون جيوفاني)
  ✅ Created: La Bohème (لا بوهيم)
  ✅ Created: The Barber of Seville (حلاق إشبيلية)
  ✅ Created: Madama Butterfly (مدام بترفلاي)

✅ Created 10 events

📅 Scheduling performances for this month...
   Creating a busy schedule with multiple events on same days...

  🎭 La Traviata:
    ✅ Monday, October 23 at 02:00 PM
    ✅ Thursday, October 26 at 03:00 PM
    ...

✅ Created 50+ performances

🎉 Days with multiple events (15+ days):

   📅 Monday, October 23:
      • 02:00 PM - La Traviata
      • 03:00 PM - Carmen
      • 05:30 PM - The Magic Flute
   ...

📊 DATABASE POPULATION SUMMARY
...
```

## After Running the Script

### 1. Start the Development Server:
```bash
python manage.py runserver
```

### 2. Access the Admin Panel:
```
http://localhost:8000/admin/
```

### 3. View Created Data:
- **Events**: Admin > Theater CMS > Events
- **Performances**: Admin > Theater CMS > Performances

### 4. Add Images (Optional):
The script creates events without images. You can add them through the admin panel:
1. Go to Events in admin
2. Click on an event
3. Upload an image in the "Image" field
4. Save

### 5. Test the Application:
- **English Home**: http://localhost:8000/home/
- **Arabic Home**: http://localhost:8000/home_ar/
- **Events List**: http://localhost:8000/events/
- **Arabic Events**: http://localhost:8000/events_ar/

## Features of Created Events

### Complete Information:
- ✅ Event title (English & Arabic)
- ✅ Composer name (English & Arabic)
- ✅ Language/subtitles info
- ✅ Conductor name
- ✅ Director name
- ✅ Duration
- ✅ Detailed "About" content (3 paragraphs)
- ✅ Full cast list with voice types
- ✅ All active and ready to display

### Performance Scheduling:
- ✅ Multiple performances per event
- ✅ Spread throughout the month
- ✅ Different times (afternoon/evening)
- ✅ Automatic date range calculation
- ✅ Ready to test calendar interface

## Notes

### ⚠️ Important:
- This script **clears all existing events and performances** before creating new ones
- Run it only in development/testing environments
- Images are not included - add them manually after running the script

### 🔄 Re-running the Script:
You can run the script multiple times. It will:
- Clear old data
- Create fresh events and performances
- Update performances for the current month

### 🎨 Customization:
To modify the script:
- Edit `events_data` in `create_events()` to change event details
- Edit `performance_times` in `create_performances()` to change show times
- Edit `num_performances` to create more/fewer shows per event

## Troubleshooting

### Error: "No module named 'theater_cms'"
**Solution**: Make sure you're running from the project root directory

### Error: "django.core.exceptions.ImproperlyConfigured"
**Solution**: Ensure Django settings are properly configured

### No performances created
**Solution**: Check that the current month has enough days for the scheduled performances

## Testing Checklist

After running the script, test:
- [ ] Events appear in admin panel
- [ ] Performances appear in admin panel
- [ ] Home page shows current event
- [ ] Events list shows all events
- [ ] Arabic versions display Arabic text
- [ ] Performance calendar shows all scheduled shows
- [ ] Can filter performances by event
- [ ] Can search events by title
- [ ] Date hierarchy works in performance admin

## Support

If you encounter any issues:
1. Check that all migrations are applied: `python manage.py migrate`
2. Verify Django settings are correct
3. Check console output for specific error messages
4. Ensure you're using the correct Python environment

---

**Happy Testing! 🎭**

