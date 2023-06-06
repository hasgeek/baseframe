# Makefile for obsolete CodeMirror 4
all: codemirror

codemirror_package = codemirror5
codemirror_ver = 4.11.0

codemirror:
	curl -L -O https://github.com/codemirror/${codemirror_package}/archive/$(codemirror_ver).zip
	unzip $(codemirror_ver).zip
	rm -rf static/js/codemirror
	mkdir static/js/codemirror
	mv ${codemirror_package}-$(codemirror_ver)/addon static/js/codemirror
	mv ${codemirror_package}-$(codemirror_ver)/keymap static/js/codemirror
	mv ${codemirror_package}-$(codemirror_ver)/lib static/js/codemirror
	mv ${codemirror_package}-$(codemirror_ver)/mode static/js/codemirror
	mv ${codemirror_package}-$(codemirror_ver)/theme static/js/codemirror
	rm -rf $(codemirror_ver).zip ${codemirror_package}-$(codemirror_ver)
