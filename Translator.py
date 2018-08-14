import polib
from openpyxl import load_workbook
from os import listdir
from os.path import isfile, join


xls_url = './translations.xlsx'
language_id_row = 1
po_files_base_url = '/Users/anieves/repos/RefWorks/pqd/src/main/resources/public/i18n/po/'
debug_translations_js_url = '/Users/anieves/repos/RefWorks/pqd/src/main/resources/public/js/translations-debug.js'
translations_js_url = '/Users/anieves/repos/RefWorks/pqd/src/main/resources/public/js/translations.js'

template_pot = '{}{}'.format(po_files_base_url, 'template.pot')
pot = polib.pofile(template_pot, encoding='utf-8-sig')
po_files_urls = dict([(f.replace('.po',''),'{}{}'.format(po_files_base_url, f)) for f in listdir(po_files_base_url) if isfile(join(po_files_base_url, f)) and f.endswith('.po')])


# Load translations from workbook
def get_translations_for_msgids(msgids):
    wb = load_workbook(xls_url)
    ws = wb['original']

    language_ids = []
    dict_translations = {}

    for idx, row in enumerate(ws.rows):
        if idx == language_id_row:
            language_ids = [cell.value for cell in row[1::]]
        if row[0].value in msgids:
            translations_values = [cell.value for cell in row[1::]]
            for idx, id in enumerate(language_ids):
                dict_translations[row[0].value] = dict(zip(language_ids, translations_values))

    return dict_translations


# Update all po files from pot and get untranslated entries
def do_translate():
    po_files = {}
    for po_lang, po_file_url in po_files_urls.items():
        po_file = polib.pofile(po_file_url, encoding='utf-8-sig')
        po_file.merge(pot)
        po_files[po_lang] = po_file
        untranslated_msgids = []
        for entry in po_file.untranslated_entries():
            untranslated_msgids.append(entry.msgid)

    # load translations
    translations_for_untranslated = get_translations_for_msgids(untranslated_msgids)
    if len(untranslated_msgids) > len(translations_for_untranslated) :
        print('Not found in XLS and pending to be translated: ')
        for not_found in [not_found for not_found in untranslated_msgids if not_found not in translations_for_untranslated ] :
            print(not_found)
    print('Untranslated strings found: ', len(untranslated_msgids))
    print('Translations found: ', len(translations_for_untranslated))
    print('')
    print('Translating...')
    # update files
    for po_lang, po_file in po_files.items():
        print('Translating file for ', po_lang)
        for entry in po_file.untranslated_entries():
            print('Looking for string: ')
            print(' ', entry.msgid)
            if entry.msgid in translations_for_untranslated:
                print(' Found:', (translations_for_untranslated[entry.msgid])[po_lang])
                entry.msgstr = (translations_for_untranslated[entry.msgid])[po_lang]
            else:
                print('TRANSLATION NOT FOUND for string', entry.msgid)
        po_file.save()
    print('...translation finished for all files')
    print('')
    print('Summary')
    #check files
    for po_lang, po_file in po_files.items():
        print('Language: ', po_lang)
        print(' Total Entries: ', len(po_file))
        print(' Translated: ', po_file.percent_translated(),'%')
        print(' Fuzzy: ', len(po_file.fuzzy_entries()))
        print(' Untranslated: ', len(po_file.untranslated_entries()))


def fix_debug_translations_js():
    content = ''
    with open(debug_translations_js_url, 'r', encoding='utf-8') as f:
        data = f.read()
        data = data.replace("'zh_cn'", "'zh'")
        data = data.replace("'zh_tw'", "'zh-tw'")
        content = data

    with open(debug_translations_js_url, 'w', encoding='utf-8') as f:
        f.write(content)

    with open(translations_js_url, 'w', encoding='utf-8') as f:
        f.write(content)

do_translate()