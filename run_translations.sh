#!/usr/bin/env bash

PQD_URL='/Users/anieves/repos/RefWorks/pqd'
CURRENT_WORKDIR=`pwd`


# Extract translations
cd $PQD_URL
grunt nggettext_extract

# Translate from xls
cd $CURRENT_WORKDIR
python3 -c 'from Translator import do_translate; do_translate()'

# Compile translations
cd $PQD_URL
grunt nggettext_compile

# Fix debug.js file
cd $CURRENT_WORKDIR
python3 -c 'from Translator import fix_debug_translations_js; fix_debug_translations_js()'