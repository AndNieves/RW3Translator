import polib
from os import listdir
from os.path import isfile, join
import json
from pprint import pprint

po_files_base_url = '/Users/anieves/repos/RefWorks/pqd/src/main/resources/public/i18n/po/'
po_files_urls = dict([(f.replace('.po', ''), '{}{}'.format(po_files_base_url, f)) for f in listdir(po_files_base_url) if
                      isfile(join(po_files_base_url, f)) and f.endswith('.po')])

json_files_base_url = '/Users/anieves/repos/RefWorks/RCM/src/assets/i18n/'
json_files_urls = dict(
    [(f.replace('.json', ''), '{}{}'.format(json_files_base_url, f)) for f in listdir(json_files_base_url) if
     isfile(join(json_files_base_url, f)) and f.endswith('.json')])



# Update all po files from pot and get untranslated entries
def get_translations():
    po_files = {}
    for po_lang, po_file_url in po_files_urls.items():
        po_file = polib.pofile(po_file_url, encoding='utf-8-sig')
        po_files[po_lang] = po_file
    return po_files
    # check files
    #for po_lang, po_file in po_files.items():



def file_to_object(url):
    with open(url, encoding='utf-8-sig') as f:
        data = json.load(f)
    return data


json_objects = {k: file_to_object(v) for k, v in json_files_urls.items()}


po_files = get_translations()

base_translation_file = 'en'


def get_translation_for(master, key, language):
    translation_key = json_objects[base_translation_file][master][key]
    translation_value = ''

    for entry in po_files[language]:
        if entry.msgid == translation_key:
            translation_value = entry.msgstr
    if translation_value == '':
        print('Translation not found for:"',translation_key, '", in language:', language)
    return translation_value


def translate_files_for_master_key(master):
    for lang, obj in json_objects.items():
        if lang == 'en':
            #Dont translate english
            continue
        
        for key, value in obj[master].items():
            if value == '':
                obj[master][key] = get_translation_for(master, key, lang)

        with open('output/'+lang+'.json', 'w', encoding='utf-8') as outfile:
            json.dump(obj, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

translate_files_for_master_key('login')

#print(get_translation_for('login', 'forgotPassword', 'es'))