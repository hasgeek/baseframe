# Makefile for sass and less stylesheets
all:
	cd baseframe; make all

babel:
	pybabel extract -F babel.cfg -k _ -k __ -k ngettext -o baseframe/translations/messages.pot .
	pybabel update -i baseframe/translations/messages.pot -d baseframe/translations
