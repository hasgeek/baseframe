# Makefile for sass and less stylesheets
all:
	cd baseframe; make all

babel:
	pybabel extract -F babel.cfg -k _ -k __ -k ngettext -o baseframe/translations/baseframe.pot .
	# these commands are needed per locale
	pybabel update -N -l hi_IN -D baseframe -i baseframe/translations/baseframe.pot -d baseframe/translations
	pybabel compile -f -D baseframe -d baseframe/translations
