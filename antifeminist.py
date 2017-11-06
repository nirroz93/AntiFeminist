import HspellPy
import re
speller = HspellPy.Hspell(linguistics=True)
text= """
אורטל בן דיין (נולדה ב-12 ביולי 1981) היא אשת תקשורת, סוציולוגית, אקטיביסטית פמיניסטית מזרחית, בלוגרית, ומעצבת אופנה.

בן דיין התפרסמה לראשונה במסגרת תביעה שלה נגד האוניברסיטה העברית בגין הטרדה מינית, אשר שינתה את התייחסות האוניברסיטה ליחסים בין סגל לסטודנטים[1], וכן את אופן הטיפול בתלונות סטודנטים על הטרדה מינית מצד חברי סגל, ונשארה בעין הציבור בשל השתתפותה בתוכניות אקטואליה ובידור בתור פנליסטית ופרשנית, הופעתה בתור דיירת בבית האח הגדול, פרסומיה בתקשורת ובעיתונות, וכן בזכות האקטיביזם שלה במגוון סוגיות חברתיות ופוליטיות.

בן דיין היא גם מעצבת ביגוד ותכשיטים, הכותבת עבור כתב העת "את" בנושאי פוליטיקה וחברה.

בן דיין נולדה בקריית שמונה בשנת 1981 למשפחה ממוצא מרוקאי. בעת שירותה הצבאי הייתה מורה חיילת, ובאותה העת כבר החלה את פעילותה החברתית במסגרת ארגוני נוער, כגון שח"ר ומהפך. סיימה ב-2006 תואר ראשון ביחסים בינלאומיים וסוציולוגיה וב-2010 תואר שני בסוציולוגיה ואנתרופולוגיה באוניברסיטה העברית, שניהם בהצטיינות.[2]

בן דיין נישאה ביוני 2016 לעיתונאי חגי מטר. באוגוסט 2017 נבחרו השניים על ידי Time Out תל אביב לרשימת "הפאוור קאפלז" (הזוגות המשפיעים) של תל אביב.[3] אלו נישואיה השניים.
"""
replacements = [
    ['היא', 'הוא'],
    ['אשת', 'איש'],
    ['שלה', 'שלו'],
]

def is_femine_linginfo(linginfos):
    return all([',נ,' in l.linginfo or 'כינוי/נ' in l.linginfo for l in linginfos])

for word in set(re.findall('[א-ת]+', text)):
    if word in speller:
        linginfos = speller.linginfo(word)

        if not linginfos: continue
        is_femine = is_femine_linginfo(linginfos)
        if not is_femine:
            continue

        only_verb = not any([not l.linginfo.startswith('פ') for l in linginfos])
        only_toar_or_noun = not any([not l.linginfo.startswith('ת,נ') for l in linginfos]) or \
                            not any([not l.linginfo.startswith('ע,נ') for l in linginfos])

        is_current = any([l.linginfo.endswith('הווה') for l in linginfos])
        #is_verb = False

        if any('כינוי/נ' in li.linginfo for li in linginfos):
            for li in linginfos:
                if li.word[-2:]=='תה':
                    replacements.append([li.word, li.word[:-2]+'תו'])
        if only_verb and not is_current:
            is_verb = [l for l in linginfos if l.linginfo.startswith('פ')]
            for verb in is_verb:
                replacements.append([verb.word, verb.stem])
        elif only_toar_or_noun:
            only_linginfos = [l for l in linginfos if l.stem!='שונות' and
                              not is_femine_linginfo([ll for ll in speller.linginfo(l.stem) if ll.linginfo.split(',', 1)[0]==l.linginfo.split(',', 1)[0]])]
            for li in only_linginfos:
                only_linginfos = [l for l in linginfos if l.stem != 'שונות']
                #print(li)
                replacements.append([li.word, li.stem])
        else:
            continue
            print(word)
            print(linginfos)

for word, rep in replacements:
    text = text.replace(word, rep)
print(text)
