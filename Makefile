# Makefile for sass and less stylesheets
all:
	cd src/baseframe; make all

babel:
	pybabel extract -F babel.cfg -k _ -k __ -k ngettext -o src/baseframe/translations/baseframe.pot .
	# these commands are needed per locale
	pybabel update -N -l hi_IN -D baseframe -i src/baseframe/translations/baseframe.pot -d src/baseframe/translations
	pybabel compile -f -D baseframe -d src/baseframe/translations
