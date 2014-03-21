#!/bin/sh
pybabel extract -F babel.cfg -k _ -k __ -k ngettext -o baseframe/translations/messages.pot .
pybabel update -D baseframe -i baseframe/translations/messages.pot -d baseframe/translations
