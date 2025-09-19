#!/usr/bin/env python
'''
Standalone Database Population Script for Lithuanian Theater CMS
Usage: python populate_db.py
'''

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theater_config.settings')
django.setup()

from theater_cms.models import Event, SeasonalSponsor, EventSponsorImage, SponsorsPageContent, Performance
from django.utils import timezone
from datetime import datetime, timedelta

def populate_database():
    '''Populate database with test data for Lithuanian theater app'''
    
    print("🎭 Populating Lithuanian Theater Database...")
    print("=" * 50)
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        Event.objects.all().delete()
        SeasonalSponsor.objects.all().delete()
        EventSponsorImage.objects.all().delete()
        Performance.objects.all().delete()
        
        # Create Events with Lithuanian content
        print("Creating events with Lithuanian translations...")
        
        events_data = [
            {
                'title': 'Rigoletto',
                'title_lt': 'Rigolettas',
                'composer': 'Giuseppe Verdi',
                'composer_lt': 'Giuseppe Verdi',
                'slug': 'rigoletto',
                'language': 'Italian with English subtitles',
                'language_lt': 'Italų kalba su lietuviškais subtitrais',
                'conductor': 'Maestro Giovanni Rossi',
                'conductor_lt': 'Maestro Giovanni Rossi',
                'director': 'Elena Martinez',
                'director_lt': 'Elena Martinez',
                'about_content': 'A tragic tale of love, betrayal, and revenge set in Renaissance Italy. This masterpiece explores themes of power, corruption, and the lengths a father will go to protect his daughter.',
                'about_content_lt': 'Tragiška meilės, išdavystės ir keršto istorija Renesanso Italijoje. Šis šedevras atskleidžia valdžios, korupcijos temas ir tai, kiek tėvas padarys, kad apsaugotų savo dukterį.',
                'cast_content': 'Featuring internationally acclaimed singers including Maria Volkov (Gilda), Roberto Martinez (Rigoletto), and Alessandro Forte (Duke of Mantua).',
                'cast_content_lt': 'Spektaklyje dalyvauja tarptautinio lygio dainininkai, įskaitant Maria Volkov (Gilda), Roberto Martinez (Rigolettas) ir Alessandro Forte (Mantujos hercogas).',
                'duration': 'Approximately 3 hours (including intermissions)',
                'duration_lt': 'Maždaug 3 valandos (įskaitant pertraukas)',
                'sort_order': 1,
                'days_from_now': 3
            },
            {
                'title': 'Aida',
                'title_lt': 'Aida',
                'composer': 'Giuseppe Verdi',
                'composer_lt': 'Giuseppe Verdi',
                'slug': 'aida',
                'language': 'Italian with English subtitles',
                'language_lt': 'Italų kalba su lietuviškais subtitrais',
                'conductor': 'Maestro Sofia Volkov',
                'conductor_lt': 'Maestro Sofia Volkov',
                'director': 'Ricardo Santos',
                'director_lt': 'Ricardo Santos',
                'about_content': 'An epic tale of love and duty set in ancient Egypt. Princess Aida must choose between her love for Radamès and loyalty to her homeland.',
                'about_content_lt': 'Epinė meilės ir pareigos istorija senovės Egipte. Princesė Aida turi rinktis tarp meilės Radamesui ir ištikimybės savo tėvynei.',
                'cast_content': 'A spectacular production featuring world-class performers and stunning Egyptian-inspired set design.',
                'cast_content_lt': 'Spektakli postanovka su pasaulinio lygio atlikėjais ir nuostabiais Egipto stiliaus dekoracijomis.',
                'duration': 'Approximately 3.5 hours (including intermissions)',
                'duration_lt': 'Maždaug 3,5 valandos (įskaitant pertraukas)',
                'sort_order': 2,
                'days_from_now': 14
            },
            {
                'title': 'La Traviata',
                'title_lt': 'Traviata',
                'composer': 'Giuseppe Verdi',
                'composer_lt': 'Giuseppe Verdi',
                'slug': 'la-traviata',
                'language': 'Italian with English subtitles',
                'language_lt': 'Italų kalba su lietuviškais subtitrais',
                'conductor': 'Maestro Alessandro Forte',
                'conductor_lt': 'Maestro Alessandro Forte',
                'director': 'Maria Petrov',
                'director_lt': 'Maria Petrov',
                'about_content': 'A heart-wrenching story of love and sacrifice in 19th century Paris. Violetta must choose between love and social conventions.',
                'about_content_lt': 'Širdį draskanti meilės ir aukos istorija XIX amžiaus Paryžiuje. Violetta turi rinktis tarp meilės ir socialinių konvencijų.',
                'cast_content': 'An intimate production showcasing vocal excellence and emotional depth.',
                'cast_content_lt': 'Intymi postanovka, demonstruojanti vokalų meistriškumą ir emocinį gilumą.',
                'duration': 'Approximately 2.5 hours (including intermissions)',
                'duration_lt': 'Maždaug 2,5 valandos (įskaitant pertraukas)',
                'sort_order': 3,
                'days_from_now': 28
            },
            {
                'title': 'The Magic Flute',
                'title_lt': 'Stebuklingas fleita',
                'composer': 'Wolfgang Amadeus Mozart',
                'composer_lt': 'Wolfgang Amadeus Mozart',
                'slug': 'magic-flute',
                'language': 'German with English subtitles',
                'language_lt': 'Vokiečių kalba su lietuviškais subtitrais',
                'conductor': 'Maestro Johann Weber',
                'conductor_lt': 'Maestro Johann Weber',
                'director': 'Anna Krueger',
                'director_lt': 'Anna Krueger',
                'about_content': 'A magical fairy tale opera filled with symbolism, beautiful arias, and Mozart\'s genius. Follow Prince Tamino on his quest to rescue Pamina.',
                'about_content_lt': 'Stebuklinga pasakų opera, pilna simbolizmo, gražių arijų ir Mocarto genijaus. Sekite princą Tamino jo kelionėje gelbėti Paminą.',
                'cast_content': 'A enchanting production perfect for opera newcomers and veterans alike.',
                'cast_content_lt': 'Žavinga postanovka, puikiai tinkanti tiek operos naujokams, tiek veteranams.',
                'duration': 'Approximately 2.5 hours (including intermissions)',
                'duration_lt': 'Maždaug 2,5 valandos (įskaitant pertraukas)',
                'sort_order': 4,
                'days_from_now': 42
            }
        ]
        
        created_events = []
        for event_data in events_data:
            days_offset = event_data.pop('days_from_now')
            start_date = timezone.now() + timedelta(days=days_offset)
            end_date = start_date + timedelta(days=7)
            
            event = Event.objects.create(
                **event_data,
                start_datetime=start_date,
                end_datetime=end_date,
                is_active=True
            )
            created_events.append(event)
            
            # Create performances for each event
            for i in range(3):  # 3 performances per event
                performance_date = start_date + timedelta(days=i*2)
                Performance.objects.create(
                    event=event,
                    start_time=performance_date.replace(hour=19, minute=30),  # 7:30 PM
                    end_time=performance_date.replace(hour=22, minute=30),    # 10:30 PM
                )
        
        print(f"✅ Created {len(created_events)} events with performances")
        
        # Create Seasonal Sponsors
        print("Creating seasonal sponsors...")
        sponsors_data = [
            {'name': 'Lexus'},
            {'name': 'OMV'},
            {'name': 'Samsung'},
            {'name': 'Rolex'}
        ]
        
        created_sponsors = []
        for sponsor_data in sponsors_data:
            sponsor = SeasonalSponsor.objects.create(**sponsor_data)
            created_sponsors.append(sponsor)
        
        print(f"✅ Created {len(created_sponsors)} seasonal sponsors")
        
        # Create Event Sponsor Images (link some events to sponsors)
        print("Creating event sponsor relationships...")
        event_sponsor_count = 0
        for event in created_events[:2]:  # First 2 events get sponsors
            for sponsor in created_sponsors[:2]:  # First 2 sponsors
                EventSponsorImage.objects.create(
                    event=event,
                    name=sponsor.name,
                    # Note: image field can be left empty for now
                )
                event_sponsor_count += 1
        
        print(f"✅ Created {event_sponsor_count} event sponsor relationships")
        
        # Ensure SponsorsPageContent exists with Lithuanian content
        print("Setting up sponsors page content...")
        sponsors_content = SponsorsPageContent.get_content()
        if not sponsors_content.sponsors_title_lt:
            sponsors_content.sponsors_title_lt = "Mūsų gerbiami rėmėjai"
        if not sponsors_content.sponsors_intro_lt:
            sponsors_content.sponsors_intro_lt = "Mūsų teatras didžiuojasi pripažindamas mūsų rėmėjų dosnų palaikymą. Jų atsidavimas menui leidžia mums tęsti mūsų puikumo tradiciją ir dalintis operos magija su žiūrovais iš viso pasaulio."
        sponsors_content.save()
        print("✅ Sponsors page content configured")
        
        print("\n🎉 Database population completed successfully!")
        print("📊 Summary:")
        print(f"   • {len(created_events)} events with Lithuanian translations")
        print(f"   • {Performance.objects.count()} scheduled performances")
        print(f"   • {len(created_sponsors)} seasonal sponsors")
        print(f"   • {event_sponsor_count} event-sponsor relationships")
        print("   • Sponsors page content with Lithuanian translations")
        
        print("\n🌐 Test your Lithuanian app at:")
        print("   • /home_lt/ (Lithuanian home page)")
        print("   • /events_lt/ (Lithuanian events listing)")
        print("   • /sponsors_lt/ (Lithuanian sponsors page)")
        print("   • /about_lt/ (Lithuanian about page)")
        
        print(f"\n🎭 Featured events:")
        for event in created_events:
            print(f"   • {event.get_title('lt')} by {event.get_composer('lt')}")
            print(f"     /event_lt/{event.slug}/ - {event.start_datetime.strftime('%B %d, %Y')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error populating database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = populate_database()
    if success:
        print("\n✅ Database populated successfully! You can now test your Lithuanian theater app.")
    else:
        print("\n❌ Database population failed. Check the error messages above.")
