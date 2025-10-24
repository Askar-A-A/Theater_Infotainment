#!/usr/bin/env python
"""
Database Population Script for Theater Infotainment System

This script populates the database with sample opera events and performances
for testing purposes. It creates 5 popular opera events with 3-5 performances
each scheduled for the current month.

Usage:
    python populate_db.py

Note: Run this from the project root directory.
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theater_config.settings')
django.setup()

from theater_cms.models import Event, Performance


def clear_existing_data():
    """Clear existing events and performances"""
    print("🗑️  Clearing existing data...")
    Performance.objects.all().delete()
    Event.objects.all().delete()
    print("✅ Existing data cleared\n")


def create_events():
    """Create 5 popular opera events"""
    print("🎭 Creating opera events...")
    
    events_data = [
        {
            'title': 'La Traviata',
            'title_ar': 'لا ترافياتا',
            'slug': 'la-traviata',
            'composer': 'Giuseppe Verdi',
            'composer_ar': 'جوزيبي فيردي',
            'language': 'Italian with English subtitles',
            'language_ar': 'الإيطالية مع ترجمة عربية',
            'conductor': 'Maestro Antonio Rossi',
            'conductor_ar': 'المايسترو أنطونيو روسي',
            'director': 'Maria Bellini',
            'director_ar': 'ماريا بيليني',
            'duration': '3 hours (including one intermission)',
            'duration_ar': '3 ساعات (بما في ذلك استراحة واحدة)',
            'about_content': '''La Traviata is one of Verdi's most beloved operas, telling the tragic love story of Violetta Valéry, a Parisian courtesan, and Alfredo Germont. This timeless masterpiece explores themes of love, sacrifice, and societal judgment.

Set in 19th century Paris, the opera follows Violetta as she falls in love with Alfredo, abandoning her life of luxury for true love. However, their happiness is short-lived when Alfredo's father convinces Violetta to leave his son to protect the family's reputation.

Our production features stunning period costumes, elaborate sets recreating the opulence of Parisian society, and world-class vocalists bringing Verdi's magnificent score to life.''',
            'about_content_ar': '''لا ترافياتا هي واحدة من أشهر أوبرات فيردي المحبوبة، تحكي قصة الحب المأساوية لفيوليتا فاليري، وهي امرأة باريسية من المجتمع الراقي، وألفريدو جيرمونت. هذه التحفة الخالدة تستكشف موضوعات الحب والتضحية والحكم المجتمعي.

تدور أحداث الأوبرا في باريس في القرن التاسع عشر، حيث تقع فيوليتا في حب ألفريدو، متخلية عن حياتها الفاخرة من أجل الحب الحقيقي. ومع ذلك، تنتهي سعادتهما بسرعة عندما يقنع والد ألفريدو فيوليتا بترك ابنه لحماية سمعة العائلة.

يتميز إنتاجنا بأزياء فترة مذهلة، ومجموعات متقنة تعيد خلق فخامة المجتمع الباريسي، ومطربين عالميين يبثون الحياة في موسيقى فيردي الرائعة.''',
            'cast_content': '''Violetta Valéry - Soprano: Elena Marchetti
Alfredo Germont - Tenor: Marco Bellini
Giorgio Germont - Baritone: Roberto Fontana
Flora Bervoix - Mezzo-soprano: Lucia Romano
Annina - Soprano: Giulia Conti''',
            'cast_content_ar': '''فيوليتا فاليري - سوبرانو: إيلينا ماركيتي
ألفريدو جيرمونت - تينور: ماركو بيليني
جورجيو جيرمونت - باريتون: روبرتو فونتانا
فلورا بيرفوا - ميزو سوبرانو: لوسيا رومانو
أنينا - سوبرانو: جوليا كونتي''',
            'is_active': True,
            'sort_order': 1
        },
        {
            'title': 'Carmen',
            'title_ar': 'كارمن',
            'slug': 'carmen',
            'composer': 'Georges Bizet',
            'composer_ar': 'جورج بيزيه',
            'language': 'French with English subtitles',
            'language_ar': 'الفرنسية مع ترجمة عربية',
            'conductor': 'Maestro Jean-Pierre Dubois',
            'conductor_ar': 'المايسترو جان بيير دوبوا',
            'director': 'Sophie Laurent',
            'director_ar': 'صوفي لوران',
            'duration': '2 hours 45 minutes (including one intermission)',
            'duration_ar': 'ساعتان و45 دقيقة (بما في ذلك استراحة واحدة)',
            'about_content': '''Carmen is Bizet's passionate tale of love, jealousy, and fate. Set in Seville, Spain, this fiery opera tells the story of the free-spirited Carmen, a gypsy woman who captivates the soldier Don José, leading to a tragic conclusion.

The opera features some of the most recognizable melodies in all of opera, including the famous "Habanera" and the "Toreador Song." Our production brings the vibrant world of 19th-century Spain to life with authentic flamenco dancing, colorful costumes, and dramatic staging.

This timeless story explores themes of freedom, passion, and the consequences of obsessive love, making it one of the most frequently performed operas worldwide.''',
            'about_content_ar': '''كارمن هي حكاية بيزيه العاطفية عن الحب والغيرة والقدر. تدور أحداثها في إشبيلية، إسبانيا، تحكي هذه الأوبرا الملتهبة قصة كارمن الحرة الروح، امرأة غجرية تأسر الجندي دون خوسيه، مما يؤدي إلى نهاية مأساوية.

تتميز الأوبرا ببعض من أشهر الألحان في عالم الأوبرا، بما في ذلك "هابانيرا" الشهيرة و"أغنية مصارع الثيران". يحيي إنتاجنا عالم إسبانيا النابض بالحياة في القرن التاسع عشر مع رقص الفلامنكو الأصيل والأزياء الملونة والإخراج الدرامي.

تستكشف هذه القصة الخالدة موضوعات الحرية والعاطفة وعواقب الحب الهوسي، مما يجعلها واحدة من أكثر الأوبرات أداءً في جميع أنحاء العالم.''',
            'cast_content': '''Carmen - Mezzo-soprano: Isabella Martinez
Don José - Tenor: Carlos Hernandez
Escamillo - Baritone: Miguel Torres
Micaëla - Soprano: Ana Garcia
Zuniga - Bass: Diego Ramirez''',
            'cast_content_ar': '''كارمن - ميزو سوبرانو: إيزابيلا مارتينيز
دون خوسيه - تينور: كارلوس هيرنانديز
إسكاميلو - باريتون: ميغيل توريس
ميكايلا - سوبرانو: آنا غارسيا
زونيغا - باص: دييغو راميريز''',
            'is_active': True,
            'sort_order': 2
        },
        {
            'title': 'The Magic Flute',
            'title_ar': 'الناي السحري',
            'slug': 'the-magic-flute',
            'composer': 'Wolfgang Amadeus Mozart',
            'composer_ar': 'فولفغانغ أماديوس موتسارت',
            'language': 'German with English subtitles',
            'language_ar': 'الألمانية مع ترجمة عربية',
            'conductor': 'Maestro Klaus Weber',
            'conductor_ar': 'المايسترو كلاوس فيبر',
            'director': 'Hans Schmidt',
            'director_ar': 'هانز شميت',
            'duration': '3 hours (including one intermission)',
            'duration_ar': '3 ساعات (بما في ذلك استراحة واحدة)',
            'about_content': '''Mozart's enchanting opera The Magic Flute is a fairy tale adventure filled with magic, mystery, and memorable music. This beloved opera combines comedy, romance, and profound symbolism in a story about Prince Tamino's quest to rescue Princess Pamina.

Guided by the magical flute and aided by the bird-catcher Papageno, Tamino must overcome trials to prove himself worthy of Pamina's love. The opera features some of Mozart's most brilliant music, including the Queen of the Night's spectacular coloratura aria.

Our family-friendly production features stunning visual effects, whimsical costumes, and imaginative sets that bring this magical world to life. Perfect for opera newcomers and seasoned enthusiasts alike.''',
            'about_content_ar': '''أوبرا موتسارت الساحرة "الناي السحري" هي مغامرة خيالية مليئة بالسحر والغموض والموسيقى التي لا تُنسى. تجمع هذه الأوبرا المحبوبة بين الكوميديا والرومانسية والرمزية العميقة في قصة عن سعي الأمير تامينو لإنقاذ الأميرة باميناً.

بتوجيه من الناي السحري وبمساعدة صائد الطيور باباجينو، يجب على تامينو التغلب على التجارب ليثبت أنه جدير بحب باميناً. تتميز الأوبرا ببعض من أروع موسيقى موتسارت، بما في ذلك أغنية ملكة الليل الكولوراتورا المذهلة.

يتميز إنتاجنا المناسب للعائلة بمؤثرات بصرية مذهلة وأزياء غريبة ومجموعات خيالية تحيي هذا العالم السحري. مثالي لمحبي الأوبرا الجدد والمتحمسين المخضرمين على حد سواء.''',
            'cast_content': '''Tamino - Tenor: Friedrich Müller
Pamina - Soprano: Greta Hoffmann
Queen of the Night - Soprano: Kristina Vogel
Papageno - Baritone: Johann Becker
Sarastro - Bass: Ludwig Braun''',
            'cast_content_ar': '''تامينو - تينور: فريدريش مولر
باميناً - سوبرانو: غريتا هوفمان
ملكة الليل - سوبرانو: كريستينا فوغل
باباجينو - باريتون: يوهان بيكر
ساراسترو - باص: لودفيغ براون''',
            'is_active': True,
            'sort_order': 3
        },
        {
            'title': 'Rigoletto',
            'title_ar': 'ريجوليتو',
            'slug': 'rigoletto',
            'composer': 'Giuseppe Verdi',
            'composer_ar': 'جوزيبي فيردي',
            'language': 'Italian with English subtitles',
            'language_ar': 'الإيطالية مع ترجمة عربية',
            'conductor': 'Maestro Paolo Caruso',
            'conductor_ar': 'المايسترو باولو كاروسو',
            'director': 'Alessandro Moretti',
            'director_ar': 'أليساندرو موريتي',
            'duration': '2 hours 30 minutes (including one intermission)',
            'duration_ar': 'ساعتان و30 دقيقة (بما في ذلك استراحة واحدة)',
            'about_content': '''Rigoletto is Verdi's powerful drama of a hunchbacked court jester whose attempts to shield his daughter from the corrupt world around them lead to tragedy. Based on Victor Hugo's play, this opera is a masterpiece of dramatic intensity and musical brilliance.

The Duke of Mantua is a womanizer who seduces Rigoletto's innocent daughter, Gilda. When Rigoletto plots revenge, his plan goes tragically wrong, leading to one of opera's most heart-wrenching conclusions.

Featuring the famous aria "La donna è mobile" and the beautiful quartet "Bella figlia dell'amore," this production showcases the dark beauty of Verdi's score with Renaissance-inspired sets and costumes that capture the decadence and danger of the Duke's court.''',
            'about_content_ar': '''ريجوليتو هي دراما فيردي القوية عن مهرج البلاط الأحدب الذي تؤدي محاولاته لحماية ابنته من العالم الفاسد من حولهم إلى المأساة. استناداً إلى مسرحية فيكتور هوغو، هذه الأوبرا هي تحفة من الكثافة الدرامية والتألق الموسيقي.

دوق مانتوا هو مغوٍ يغوي ابنة ريجوليتو البريئة، جيلدا. عندما يخطط ريجوليتو للانتقام، تسوء خطته بشكل مأساوي، مما يؤدي إلى واحدة من أكثر النهايات حزناً في الأوبرا.

تتميز بالأغنية الشهيرة "لا دونا إي موبيلي" والرباعية الجميلة "بيلا فيليا ديل أموري"، يعرض هذا الإنتاج الجمال المظلم لموسيقى فيردي مع مجموعات وأزياء مستوحاة من عصر النهضة تلتقط انحطاط وخطر بلاط الدوق.''',
            'cast_content': '''Rigoletto - Baritone: Luca Salsi
Duke of Mantua - Tenor: Vittorio Grigolo
Gilda - Soprano: Francesca Dotto
Sparafucile - Bass: Riccardo Zanellato
Maddalena - Contralto: Veronica Simeoni''',
            'cast_content_ar': '''ريجوليتو - باريتون: لوكا سالسي
دوق مانتوا - تينور: فيتوريو غريغولو
جيلدا - سوبرانو: فرانشيسكا دوتو
سبارافوتشيلي - باص: ريكاردو زانيلاتو
مادالينا - كونترالتو: فيرونيكا سيميوني''',
            'is_active': True,
            'sort_order': 4
        },
        {
            'title': 'Tosca',
            'title_ar': 'توسكا',
            'slug': 'tosca',
            'composer': 'Giacomo Puccini',
            'composer_ar': 'جياكومو بوتشيني',
            'language': 'Italian with English subtitles',
            'language_ar': 'الإيطالية مع ترجمة عربية',
            'conductor': 'Maestro Riccardo Muti',
            'conductor_ar': 'المايسترو ريكاردو موتي',
            'director': 'Franco Zeffirelli',
            'director_ar': 'فرانكو زيفيريللي',
            'duration': '2 hours 45 minutes (including one intermission)',
            'duration_ar': 'ساعتان و45 دقيقة (بما في ذلك استراحة واحدة)',
            'about_content': '''Tosca is Puccini's thrilling tale of love, lust, murder, and political intrigue set in Rome during the Napoleonic wars. This intense opera follows the tragic fate of the beautiful opera singer Floria Tosca, her lover Mario Cavaradossi, and the villainous police chief Baron Scarpia.

When Cavaradossi is arrested for harboring a political fugitive, Scarpia offers to spare his life in exchange for Tosca's affections. The opera builds to a dramatic climax featuring some of opera's most powerful moments, including Tosca's famous aria "Vissi d'arte."

Our production features authentic Roman locations recreated on stage, including the Church of Sant'Andrea della Valle, the Farnese Palace, and the Castel Sant'Angelo. The stunning sets combined with Puccini's passionate score create an unforgettable theatrical experience.''',
            'about_content_ar': '''توسكا هي حكاية بوتشيني المثيرة عن الحب والشهوة والقتل والمؤامرات السياسية التي تدور أحداثها في روما خلال الحروب النابليونية. تتبع هذه الأوبرا المكثفة المصير المأساوي لمغنية الأوبرا الجميلة فلوريا توسكا، وحبيبها ماريو كافاراداسي، ورئيس الشرطة الشرير البارون سكاربيا.

عندما يُعتقل كافاراداسي لإيواء هارب سياسي، يعرض سكاربيا إنقاذ حياته مقابل عواطف توسكا. تتصاعد الأوبرا إلى ذروة درامية تتضمن بعضاً من أقوى لحظات الأوبرا، بما في ذلك أغنية توسكا الشهيرة "فيسي دارتي".

يتميز إنتاجنا بمواقع رومانية أصيلة معاد إنشاؤها على المسرح، بما في ذلك كنيسة سانت أندريا ديلا فالي، وقصر فارنيزي، وقلعة سانت أنجيلو. تخلق المجموعات المذهلة جنباً إلى جنب مع موسيقى بوتشيني العاطفية تجربة مسرحية لا تُنسى.''',
            'cast_content': '''Floria Tosca - Soprano: Anna Netrebko
Mario Cavaradossi - Tenor: Jonas Kaufmann
Baron Scarpia - Baritone: Bryn Terfel
Cesare Angelotti - Bass: Ain Anger
Sacristan - Baritone: Carlo Bosi''',
            'cast_content_ar': '''فلوريا توسكا - سوبرانو: آنا نتريبكو
ماريو كافاراداسي - تينور: يوناس كاوفمان
البارون سكاربيا - باريتون: برين تيرفيل
تشيزاري أنجيلوتي - باص: آين أنجر
القسيس - باريتون: كارلو بوزي''',
            'is_active': True,
            'sort_order': 5
        },
        {
            'title': 'Aida',
            'title_ar': 'عايدة',
            'slug': 'aida',
            'composer': 'Giuseppe Verdi',
            'composer_ar': 'جوزيبي فيردي',
            'language': 'Italian with English subtitles',
            'language_ar': 'الإيطالية مع ترجمة عربية',
            'conductor': 'Maestro Fabio Luisi',
            'conductor_ar': 'المايسترو فابيو لويزي',
            'director': 'Sonja Frisell',
            'director_ar': 'سونيا فريسيل',
            'duration': '3 hours 15 minutes (including two intermissions)',
            'duration_ar': '3 ساعات و15 دقيقة (بما في ذلك استراحتين)',
            'about_content': '''Aida is Verdi's grand opera set in ancient Egypt, telling the story of forbidden love between Radamès, an Egyptian military commander, and Aida, an enslaved Ethiopian princess. This spectacular opera combines romance, political intrigue, and stunning pageantry.

Commissioned to celebrate the opening of the Suez Canal, Aida features some of Verdi's most memorable music, including the famous "Triumphal March" and Aida's heartbreaking aria "O patria mia." The opera explores themes of love, duty, and sacrifice against the backdrop of war between Egypt and Ethiopia.

Our production features elaborate Egyptian-inspired sets, hundreds of costumes, and a cast of over 100 performers including chorus, dancers, and musicians. The grand scale and emotional depth make this one of opera's most beloved masterpieces.''',
            'about_content_ar': '''عايدة هي أوبرا فيردي الكبرى التي تدور أحداثها في مصر القديمة، تحكي قصة الحب المحرم بين رادامس، القائد العسكري المصري، وعايدة، الأميرة الإثيوبية المستعبدة. تجمع هذه الأوبرا المذهلة بين الرومانسية والمؤامرات السياسية والاحتفالات المبهرة.

تم تكليف عايدة للاحتفال بافتتاح قناة السويس، وتتميز ببعض من أشهر موسيقى فيردي، بما في ذلك "مسيرة النصر" الشهيرة وأغنية عايدة المؤثرة "يا وطني". تستكشف الأوبرا موضوعات الحب والواجب والتضحية على خلفية الحرب بين مصر وإثيوبيا.

يتميز إنتاجنا بمجموعات متقنة مستوحاة من مصر القديمة، ومئات الأزياء، وفريق من أكثر من 100 فنان بما في ذلك الكورس والراقصين والموسيقيين. الحجم الكبير والعمق العاطفي يجعلان هذه واحدة من أكثر روائع الأوبرا المحبوبة.''',
            'cast_content': '''Aida - Soprano: Liudmyla Monastyrska
Radamès - Tenor: Roberto Alagna
Amneris - Mezzo-soprano: Anita Rachvelishvili
Amonasro - Baritone: George Gagnidze
Ramfis - Bass: Dmitry Belosselskiy''',
            'cast_content_ar': '''عايدة - سوبرانو: ليودميلا موناستيرسكا
رادامس - تينور: روبرتو ألانيا
أمنيريس - ميزو سوبرانو: أنيتا راشفيليشفيلي
أموناسرو - باريتون: جورج غاغنيدزي
رامفيس - باص: دميتري بيلوسيلسكي''',
            'is_active': True,
            'sort_order': 6
        },
        {
            'title': 'Don Giovanni',
            'title_ar': 'دون جيوفاني',
            'slug': 'don-giovanni',
            'composer': 'Wolfgang Amadeus Mozart',
            'composer_ar': 'فولفغانغ أماديوس موتسارت',
            'language': 'Italian with English subtitles',
            'language_ar': 'الإيطالية مع ترجمة عربية',
            'conductor': 'Maestro Yannick Nézet-Séguin',
            'conductor_ar': 'المايسترو يانيك نيزيه-سيغان',
            'director': 'Michael Grandage',
            'director_ar': 'مايكل غراندج',
            'duration': '3 hours (including one intermission)',
            'duration_ar': '3 ساعات (بما في ذلك استراحة واحدة)',
            'about_content': '''Don Giovanni is Mozart's dark comedy about the infamous libertine Don Giovanni and his endless pursuit of women. This dramma giocoso masterfully blends comedy and tragedy, exploring themes of seduction, morality, and divine retribution.

The unrepentant Don Giovanni, aided by his servant Leporello, leaves a trail of broken hearts until he faces supernatural justice. The opera features some of Mozart's most brilliant music, from the seductive "Là ci darem la mano" to the terrifying finale with the Stone Guest.

Our modern production sets the action in contemporary times while preserving Mozart's timeless music. The staging emphasizes the psychological complexity of the characters and the opera's exploration of power, desire, and consequence.''',
            'about_content_ar': '''دون جيوفاني هي كوميديا موتسارت المظلمة عن الفاسق الشهير دون جيوفاني وسعيه اللامتناهي وراء النساء. تمزج هذه التحفة الدرامية الكوميدية ببراعة بين الكوميديا والمأساة، مستكشفة موضوعات الإغواء والأخلاق والعقاب الإلهي.

دون جيوفاني غير النادم، بمساعدة خادمه ليبوريللو، يترك وراءه أثراً من القلوب المكسورة حتى يواجه العدالة الخارقة للطبيعة. تتميز الأوبرا ببعض من أروع موسيقى موتسارت، من الأغنية المغرية "لا تشي داريم لا مانو" إلى النهاية المرعبة مع الضيف الحجري.

يضع إنتاجنا الحديث الأحداث في العصر المعاصر مع الحفاظ على موسيقى موتسارت الخالدة. يؤكد الإخراج على التعقيد النفسي للشخصيات واستكشاف الأوبرا للسلطة والرغبة والعواقب.''',
            'cast_content': '''Don Giovanni - Baritone: Ildebrando D'Arcangelo
Leporello - Bass: Luca Pisaroni
Donna Anna - Soprano: Malin Byström
Don Ottavio - Tenor: Paul Appleby
Donna Elvira - Soprano: Hibla Gerzmava''',
            'cast_content_ar': '''دون جيوفاني - باريتون: إلديبراندو دارشانجيلو
ليبوريللو - باص: لوكا بيزاروني
دونا آنا - سوبرانو: مالين بيستروم
دون أوتافيو - تينور: بول أبليبي
دونا إلفيرا - سوبرانو: هيبلا جيرزمافا''',
            'is_active': True,
            'sort_order': 7
        },
        {
            'title': 'La Bohème',
            'title_ar': 'لا بوهيم',
            'slug': 'la-boheme',
            'composer': 'Giacomo Puccini',
            'composer_ar': 'جياكومو بوتشيني',
            'language': 'Italian with English subtitles',
            'language_ar': 'الإيطالية مع ترجمة عربية',
            'conductor': 'Maestro Marco Armiliato',
            'conductor_ar': 'المايسترو ماركو أرميلياتو',
            'director': 'Franco Zeffirelli',
            'director_ar': 'فرانكو زيفيريللي',
            'duration': '2 hours 30 minutes (including one intermission)',
            'duration_ar': 'ساعتان و30 دقيقة (بما في ذلك استراحة واحدة)',
            'about_content': '''La Bohème is Puccini's beloved masterpiece about young love and loss in 1830s Paris. Following a group of impoverished artists in the Latin Quarter, the opera tells the touching love story of the poet Rodolfo and the seamstress Mimì.

The opera captures the joy and sorrow of bohemian life with some of opera's most beautiful music, including "Che gelida manina," "Mi chiamano Mimì," and the heartbreaking final scene. Puccini's score perfectly captures both the carefree spirit of youth and the tragedy of Mimì's illness.

Our classic production recreates the romance and atmosphere of 19th-century Paris with detailed period sets and costumes. This timeless story of love, friendship, and sacrifice continues to move audiences worldwide.''',
            'about_content_ar': '''لا بوهيم هي تحفة بوتشيني المحبوبة عن الحب الشاب والفقدان في باريس في ثلاثينيات القرن التاسع عشر. تتبع مجموعة من الفنانين الفقراء في الحي اللاتيني، تحكي الأوبرا قصة الحب المؤثرة بين الشاعر رودولفو والخياطة ميمي.

تلتقط الأوبرا فرحة وحزن الحياة البوهيمية ببعض من أجمل موسيقى الأوبرا، بما في ذلك "كي جيليدا مانينا" و"مي كيامانو ميمي" والمشهد الأخير المفجع. تلتقط موسيقى بوتشيني بشكل مثالي كلاً من روح الشباب الخالية من الهموم ومأساة مرض ميمي.

يعيد إنتاجنا الكلاسيكي خلق رومانسية وأجواء باريس في القرن التاسع عشر مع مجموعات وأزياء تفصيلية من تلك الفترة. تستمر هذه القصة الخالدة عن الحب والصداقة والتضحية في تحريك الجماهير في جميع أنحاء العالم.''',
            'cast_content': '''Mimì - Soprano: Sonya Yoncheva
Rodolfo - Tenor: Michael Fabiano
Marcello - Baritone: Lucas Meachem
Musetta - Soprano: Susanna Phillips
Colline - Bass: Christian Van Horn''',
            'cast_content_ar': '''ميمي - سوبرانو: سونيا يونشيفا
رودولفو - تينور: مايكل فابيانو
مارسيلو - باريتون: لوكاس ميتشم
موزيتا - سوبرانو: سوزانا فيليبس
كولين - باص: كريستيان فان هورن''',
            'is_active': True,
            'sort_order': 8
        },
        {
            'title': 'The Barber of Seville',
            'title_ar': 'حلاق إشبيلية',
            'slug': 'the-barber-of-seville',
            'composer': 'Gioachino Rossini',
            'composer_ar': 'جواكينو روسيني',
            'language': 'Italian with English subtitles',
            'language_ar': 'الإيطالية مع ترجمة عربية',
            'conductor': 'Maestro Michele Mariotti',
            'conductor_ar': 'المايسترو ميكيلي ماريوتي',
            'director': 'Bartlett Sher',
            'director_ar': 'بارتليت شير',
            'duration': '3 hours (including one intermission)',
            'duration_ar': '3 ساعات (بما في ذلك استراحة واحدة)',
            'about_content': '''The Barber of Seville is Rossini's sparkling comic masterpiece about love, disguise, and clever schemes in 18th-century Seville. Count Almaviva enlists the help of the resourceful barber Figaro to win the heart of the beautiful Rosina, who is kept under lock and key by her guardian, Dr. Bartolo.

Filled with mistaken identities, hilarious situations, and brilliant vocal fireworks, the opera features some of the most famous music in all of opera, including Figaro's irrepressible "Largo al factotum" and Rosina's charming "Una voce poco fa."

Our vibrant production captures the wit and energy of Rossini's score with colorful sets, period costumes, and athletic staging that brings out the physical comedy of this beloved opera buffa.''',
            'about_content_ar': '''حلاق إشبيلية هي تحفة روسيني الكوميدية المتألقة عن الحب والتنكر والمكائد الذكية في إشبيلية في القرن الثامن عشر. يستعين الكونت ألمافيفا بمساعدة الحلاق الماهر فيغارو للفوز بقلب روزينا الجميلة، التي يحتفظ بها وصيها الدكتور بارتولو تحت الحراسة المشددة.

مليئة بالهويات المخطئة والمواقف المضحكة والألعاب النارية الصوتية الرائعة، تتميز الأوبرا ببعض من أشهر الموسيقى في عالم الأوبرا، بما في ذلك أغنية فيغارو التي لا تقاوم "لارغو آل فاكتوتوم" وأغنية روزينا الساحرة "أونا فوتشي بوكو فا".

يلتقط إنتاجنا النابض بالحياة ذكاء وطاقة موسيقى روسيني مع مجموعات ملونة وأزياء من تلك الفترة وإخراج رياضي يبرز الكوميديا الجسدية لهذه الأوبرا البوفا المحبوبة.''',
            'cast_content': '''Figaro - Baritone: Andrzej Filończyk
Count Almaviva - Tenor: Javier Camarena
Rosina - Mezzo-soprano: Isabel Leonard
Dr. Bartolo - Bass: Maurizio Muraro
Don Basilio - Bass: Alexander Vinogradov''',
            'cast_content_ar': '''فيغارو - باريتون: أندريه فيلونتشيك
الكونت ألمافيفا - تينور: خافيير كاماريناً
روزينا - ميزو سوبرانو: إيزابيل ليونارد
الدكتور بارتولو - باص: ماوريتسيو مورارو
دون باسيليو - باص: ألكسندر فينوغرادوف''',
            'is_active': True,
            'sort_order': 9
        },
        {
            'title': 'Madama Butterfly',
            'title_ar': 'مدام بترفلاي',
            'slug': 'madama-butterfly',
            'composer': 'Giacomo Puccini',
            'composer_ar': 'جياكومو بوتشيني',
            'language': 'Italian with English subtitles',
            'language_ar': 'الإيطالية مع ترجمة عربية',
            'conductor': 'Maestro Pier Giorgio Morandi',
            'conductor_ar': 'المايسترو بيير جورجيو موراندي',
            'director': 'Anthony Minghella',
            'director_ar': 'أنتوني مينغيلا',
            'duration': '2 hours 45 minutes (including one intermission)',
            'duration_ar': 'ساعتان و45 دقيقة (بما في ذلك استراحة واحدة)',
            'about_content': '''Madama Butterfly is Puccini's heartbreaking tale of love and betrayal set in early 20th-century Japan. The young geisha Cio-Cio-San (Butterfly) falls in love with American naval officer Pinkerton, who abandons her after their marriage, leaving her to wait faithfully for his return.

Three years later, Pinkerton returns with his American wife, leading to one of opera's most tragic conclusions. The opera features Puccini's most beautiful and emotional music, including the famous "Un bel dì vedremo" and the devastating final scene.

Our production features stunning Japanese-inspired sets and costumes, authentic cultural details, and sensitive staging that honors both the beauty and tragedy of Butterfly's story. This powerful opera explores themes of cultural clash, devotion, and sacrifice.''',
            'about_content_ar': '''مدام بترفلاي هي حكاية بوتشيني المفجعة عن الحب والخيانة التي تدور أحداثها في اليابان في أوائل القرن العشرين. تقع الجيشا الشابة تشيو-تشيو-سان (بترفلاي) في حب الضابط البحري الأمريكي بينكرتون، الذي يتخلى عنها بعد زواجهما، تاركاً إياها تنتظر بأمانة عودته.

بعد ثلاث سنوات، يعود بينكرتون مع زوجته الأمريكية، مما يؤدي إلى واحدة من أكثر النهايات مأساوية في الأوبرا. تتميز الأوبرا بأجمل وأكثر موسيقى بوتشيني عاطفية، بما في ذلك الأغنية الشهيرة "أون بيل دي فيدريمو" والمشهد الأخير المدمر.

يتميز إنتاجنا بمجموعات وأزياء مذهلة مستوحاة من اليابان، وتفاصيل ثقافية أصيلة، وإخراج حساس يكرم كلاً من جمال ومأساة قصة بترفلاي. تستكشف هذه الأوبرا القوية موضوعات الصدام الثقافي والإخلاص والتضحية.''',
            'cast_content': '''Cio-Cio-San (Butterfly) - Soprano: Hui He
Pinkerton - Tenor: Andrea Carè
Sharpless - Baritone: Paulo Szot
Suzuki - Mezzo-soprano: Maria Zifchak
Goro - Tenor: Tony Stevenson''',
            'cast_content_ar': '''تشيو-تشيو-سان (بترفلاي) - سوبرانو: هوي هي
بينكرتون - تينور: أندريا كاريه
شاربليس - باريتون: باولو زوت
سوزوكي - ميزو سوبرانو: ماريا زيفشاك
غورو - تينور: توني ستيفنسون''',
            'is_active': True,
            'sort_order': 10
        }
    ]
    
    created_events = []
    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            slug=event_data['slug'],
            defaults=event_data
        )
        if created:
            print(f"  ✅ Created: {event.title} ({event.title_ar})")
        else:
            print(f"  ℹ️  Already exists: {event.title}")
        created_events.append(event)
    
    print(f"\n✅ Created {len(created_events)} events\n")
    return created_events


def create_performances(events):
    """Create 4-6 performances for each event with tighter scheduling and multiple events per day"""
    print("📅 Scheduling performances for this month...")
    print("   Creating a busy schedule with multiple events on same days...\n")
    
    # Get current date and calculate month boundaries
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    
    # Performance times - expanded for tighter scheduling
    performance_times = [
        (14, 0),  # 2:00 PM (matinee)
        (15, 0),  # 3:00 PM (afternoon)
        (17, 30), # 5:30 PM (early evening)
        (18, 0),  # 6:00 PM (evening)
        (19, 0),  # 7:00 PM (evening)
        (19, 30), # 7:30 PM (late evening)
    ]
    
    performances_created = 0
    performances_by_date = {}  # Track performances by date for summary
    
    # Calculate how many days we have in the current month
    if current_month == 12:
        next_month_date = datetime(current_year + 1, 1, 1)
    else:
        next_month_date = datetime(current_year, current_month + 1, 1)
    
    days_in_month = (next_month_date - datetime(current_year, current_month, 1)).days
    
    for event in events:
        # Create 4-6 performances per event (more for popular operas)
        if event.sort_order <= 3:
            num_performances = 6  # First 3 events get 6 performances
        elif event.sort_order <= 6:
            num_performances = 5  # Next 3 events get 5 performances
        else:
            num_performances = 4  # Last 4 events get 4 performances
        
        print(f"  🎭 {event.title}:")
        
        for i in range(num_performances):
            # Tighter scheduling: performances every 3-4 days instead of 7
            # Offset by event sort_order to create variety and overlaps
            day_offset = (i * 3) + (event.sort_order % 5)
            
            # Make sure we don't go past the end of the month
            try:
                performance_date = datetime(current_year, current_month, 1) + timedelta(days=day_offset)
                
                # Skip if we've gone into next month
                if performance_date.month != current_month or performance_date.day > days_in_month:
                    continue
                
                # Choose time - vary based on event and performance index
                # This creates natural overlaps where different events happen on same day
                time_index = (event.sort_order + i) % len(performance_times)
                hour, minute = performance_times[time_index]
                
                start_time = timezone.make_aware(datetime(
                    performance_date.year,
                    performance_date.month,
                    performance_date.day,
                    hour,
                    minute
                ))
                
                # End time is 3 hours later (typical opera duration)
                end_time = start_time + timedelta(hours=3)
                
                # Create performance
                performance = Performance.objects.create(
                    event=event,
                    start_time=start_time,
                    end_time=end_time
                )
                
                performances_created += 1
                date_key = start_time.strftime('%Y-%m-%d')
                
                # Track for summary
                if date_key not in performances_by_date:
                    performances_by_date[date_key] = []
                performances_by_date[date_key].append({
                    'event': event.title,
                    'time': start_time.strftime('%I:%M %p')
                })
                
                print(f"    ✅ {start_time.strftime('%A, %B %d at %I:%M %p')}")
                
            except ValueError:
                # Skip invalid dates (e.g., Feb 30)
                continue
    
    print(f"\n✅ Created {performances_created} performances")
    
    # Show days with multiple events
    multi_event_days = {k: v for k, v in performances_by_date.items() if len(v) > 1}
    if multi_event_days:
        print(f"\n🎉 Days with multiple events ({len(multi_event_days)} days):")
        for date_key in sorted(multi_event_days.keys())[:5]:  # Show first 5
            date_obj = datetime.strptime(date_key, '%Y-%m-%d')
            print(f"\n   📅 {date_obj.strftime('%A, %B %d')}:")
            for perf in sorted(multi_event_days[date_key], key=lambda x: x['time']):
                print(f"      • {perf['time']} - {perf['event']}")
        if len(multi_event_days) > 5:
            print(f"   ... and {len(multi_event_days) - 5} more days with multiple events")
    
    print()
    return performances_created


def display_summary(events):
    """Display a summary of created data"""
    print("\n" + "="*70)
    print("📊 DATABASE POPULATION SUMMARY")
    print("="*70)
    
    print(f"\n🎭 Events Created: {len(events)}")
    for event in events:
        performances = Performance.objects.filter(event=event).order_by('start_time')
        print(f"\n  {event.title} ({event.title_ar})")
        print(f"  Composer: {event.composer}")
        print(f"  Performances: {performances.count()}")
        if performances.exists():
            print(f"  First show: {performances.first().start_time.strftime('%B %d, %Y at %I:%M %p')}")
            print(f"  Last show: {performances.last().start_time.strftime('%B %d, %Y at %I:%M %p')}")
    
    total_performances = Performance.objects.count()
    print(f"\n📅 Total Performances: {total_performances}")
    
    print("\n" + "="*70)
    print("✅ Database population completed successfully!")
    print("="*70)
    print("\n💡 Next steps:")
    print("  1. Run the development server: python manage.py runserver")
    print("  2. Access admin panel: http://localhost:8000/admin/")
    print("  3. View performances: Admin > Performances")
    print("  4. Add event images through the admin panel")
    print("\n")


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("🎭 THEATER INFOTAINMENT DATABASE POPULATION SCRIPT")
    print("="*70 + "\n")
    
    try:
        # Step 1: Clear existing data
        clear_existing_data()
        
        # Step 2: Create events
        events = create_events()
        
        # Step 3: Create performances
        create_performances(events)
        
        # Step 4: Display summary
        display_summary(events)
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

