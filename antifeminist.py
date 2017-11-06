import sys
from flask import Flask, request
import urllib.request
import urllib.parse
import HspellPy
import re


def femine(text):
    # manual repalcements
    replacements = [
        ['היא', 'הוא'],
        ['אשת', 'איש'],
        ['שלה', 'שלו'],
    ]

    speller = HspellPy.Hspell(linguistics=True)

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
            replacements+=[([li.word, li.word[:-2] + 'תו']) for li in linginfos if 'כינוי/נ' in li.linginfo and li.word[-2:] == 'תה']
            if only_verb and not is_current:
                is_verb = [l for l in linginfos if l.linginfo.startswith('פ')]
                for verb in is_verb:
                    replacements.append([verb.word, verb.stem])
            elif only_toar_or_noun:
                if(any(l.linginfo.endswith('סמיכות') for l in linginfos)):
                    continue
                only_linginfos = [l for l in linginfos if l.stem != 'שונות' and
                                  not is_femine_linginfo([ll for ll in speller.linginfo(l.stem) if
                                                          ll.linginfo.split(',', 1)[0] == l.linginfo.split(',', 1)[0]])]
                for li in only_linginfos:
                    replacements.append([li.word, li.stem])
            else:
                continue
                print(word)
                print(linginfos)

    for word, rep in replacements:
        text = text.replace(word, rep)
    return (text)

app = Flask(__name__)


@app.route('/antiFemine', methods=['GET', 'POST'])
def antiFemine():
    if 'text' in request.args:
        text = request.args.get('text')
        return femine(text)
    elif 'url' in request.args:
        urlEnc = urllib.parse.quote(request.args.get('url'), safe='/:')
        with urllib.request.urlopen(urlEnc) as res:
            html_content = res.read()
            encoding = res.headers.get_content_charset('utf-8')
            html_text = html_content.decode(encoding)
        return (femine(html_text))
    else:
        return "No text"


if (__name__ == "__main__"):
    app.run()
