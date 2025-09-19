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
    '''Populate database with test data for Russian theater app'''
    
    print("🎭 Populating Russian Theater Database...")
    print("=" * 50)
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        Event.objects.all().delete()
        SeasonalSponsor.objects.all().delete()
        EventSponsorImage.objects.all().delete()
        Performance.objects.all().delete()
        
        # Create Events with Russian content
        print("Creating events with Russian translations...")
        
        events_data = [
            {
                'title': 'Rigoletto',
                'title_ru': 'Риголетто',
                'composer': 'Giuseppe Verdi',
                'composer_ru': 'Джузеппе Верди',
                'slug': 'rigoletto',
                'language': 'Italian with English subtitles',
                'language_ru': 'На итальянском языке с русскими субтитрами',
                'conductor': 'Maestro Giovanni Rossi',
                'conductor_ru': 'Маэстро Джованни Росси',
                'director': 'Elena Martinez',
                'director_ru': 'Елена Мартинес',
                'about_content': 'A tragic tale of love, betrayal, and revenge set in Renaissance Italy. This masterpiece explores themes of power, corruption, and the lengths a father will go to protect his daughter.',
                'about_content_ru': 'Трагическая история любви, предательства и мести в эпоху Возрождения в Италии. Этот шедевр исследует темы власти, коррупции и того, на что готов пойти отец, чтобы защитить свою дочь.',
                'cast_content': 'Featuring internationally acclaimed singers including Maria Volkov (Gilda), Roberto Martinez (Rigoletto), and Alessandro Forte (Duke of Mantua).',
                'cast_content_ru': 'В постановке участвуют всемирно признанные певцы, включая Марию Волкову (Джильда), Роберто Мартинеса (Риголетто) и Алессандро Форте (Герцог Мантуанский).',
                'duration': 'Approximately 3 hours (including intermissions)',
                'duration_ru': 'Примерно 3 часа (включая антракты)',
                'sort_order': 1,
                'days_from_now': 3
            },
            {
                'title': 'Aida',
                'title_ru': 'Аида',
                'composer': 'Giuseppe Verdi',
                'composer_ru': 'Джузеппе Верди',
                'slug': 'aida',
                'language': 'Italian with English subtitles',
                'language_ru': 'На итальянском языке с русскими субтитрами',
                'conductor': 'Maestro Sofia Volkov',
                'conductor_ru': 'Маэстро София Волкова',
                'director': 'Ricardo Santos',
                'director_ru': 'Рикардо Сантос',
                'about_content': 'An epic tale of love and duty set in ancient Egypt. Princess Aida must choose between her love for Radamès and loyalty to her homeland.',
                'about_content_ru': 'Эпическая история любви и долга в древнем Египте. Принцесса Аида должна выбирать между любовью к Радамесу и верностью своей родине.',
                'cast_content': 'A spectacular production featuring world-class performers and stunning Egyptian-inspired set design.',
                'cast_content_ru': 'Захватывающая постановка с участием исполнителей мирового класса и потрясающими декорациями в египетском стиле.',
                'duration': 'Approximately 3.5 hours (including intermissions)',
                'duration_ru': 'Примерно 3,5 часа (включая антракты)',
                'sort_order': 2,
                'days_from_now': 14
            },
            {
                'title': 'La Traviata',
                'title_ru': 'Травиата',
                'composer': 'Giuseppe Verdi',
                'composer_ru': 'Джузеппе Верди',
                'slug': 'la-traviata',
                'language': 'Italian with English subtitles',
                'language_ru': 'На итальянском языке с русскими субтитрами',
                'conductor': 'Maestro Alessandro Forte',
                'conductor_ru': 'Маэстро Алессандро Форте',
                'director': 'Maria Petrov',
                'director_ru': 'Мария Петрова',
                'about_content': 'A heart-wrenching story of love and sacrifice in 19th century Paris. Violetta must choose between love and social conventions.',
                'about_content_ru': 'Душераздирающая история любви и жертвы в Париже XIX века. Виолетта должна выбирать между любовью и социальными условностями.',
                'cast_content': 'An intimate production showcasing vocal excellence and emotional depth.',
                'cast_content_ru': 'Интимная постановка, демонстрирующая вокальное мастерство и эмоциональную глубину.',
                'duration': 'Approximately 2.5 hours (including intermissions)',
                'duration_ru': 'Примерно 2,5 часа (включая антракты)',
                'sort_order': 3,
                'days_from_now': 28
            },
            {
                'title': 'The Magic Flute',
                'title_ru': 'Волшебная флейта',
                'composer': 'Wolfgang Amadeus Mozart',
                'composer_ru': 'Вольфганг Амадей Моцарт',
                'slug': 'magic-flute',
                'language': 'German with English subtitles',
                'language_ru': 'На немецком языке с русскими субтитрами',
                'conductor': 'Maestro Johann Weber',
                'conductor_ru': 'Маэстро Йоханн Вебер',
                'director': 'Anna Krueger',
                'director_ru': 'Анна Крюгер',
                'about_content': 'A magical fairy tale opera filled with symbolism, beautiful arias, and Mozart\'s genius. Follow Prince Tamino on his quest to rescue Pamina.',
                'about_content_ru': 'Волшебная сказочная опера, полная символизма, прекрасных арий и гениальности Моцарта. Следите за принцем Тамино в его поисках спасения Памины.',
                'cast_content': 'A enchanting production perfect for opera newcomers and veterans alike.',
                'cast_content_ru': 'Очаровательная постановка, идеальная как для новичков в опере, так и для ветеранов.',
                'duration': 'Approximately 2.5 hours (including intermissions)',
                'duration_ru': 'Примерно 2,5 часа (включая антракты)',
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
        
        # Ensure SponsorsPageContent exists with Russian content
        print("Setting up sponsors page content...")
        sponsors_content = SponsorsPageContent.get_content()
        if not sponsors_content.sponsors_title_ru:
            sponsors_content.sponsors_title_ru = "Наши уважаемые спонсоры"
        if not sponsors_content.sponsors_intro_ru:
            sponsors_content.sponsors_intro_ru = "Наш театр с гордостью выражает благодарность нашим спонсорам за их щедрую поддержку. Их преданность искусству позволяет нам продолжать традицию совершенства и делиться волшебством оперы со зрителями со всего мира."
        sponsors_content.save()
        print("✅ Sponsors page content configured")
        
        print("\\n🎉 Database population completed successfully!")
        print("📊 Summary:")
        print(f"   • {len(created_events)} events with Russian translations")
        print(f"   • {Performance.objects.count()} scheduled performances")
        print(f"   • {len(created_sponsors)} seasonal sponsors")
        print(f"   • {event_sponsor_count} event-sponsor relationships")
        print("   • Sponsors page content with Russian translations")
        
        print("\\n🌐 Test your Russian app at:")
        print("   • /home_ru/ (Russian home page)")
        print("   • /events_ru/ (Russian events listing)")
        print("   • /sponsors_ru/ (Russian sponsors page)")
        print("   • /about_ru/ (Russian about page)")
        
        print(f"\\n🎭 Featured events:")
        for event in created_events:
            print(f"   • {event.get_title('ru')} by {event.get_composer('ru')}")
            print(f"     /event_ru/{event.slug}/ - {event.start_datetime.strftime('%B %d, %Y')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error populating database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = populate_database()
    if success:
        print("\\n✅ Database populated successfully! You can now test your Russian theater app.")
    else:
        print("\\n❌ Database population failed. Check the error messages above.")
