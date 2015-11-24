# Makefile for tinymce
all: tinymce codemirror

tinymce3_zip = tinymce_3.5.11_jquery.zip
tinymce4_zip = tinymce_4.3.0_jquery.zip
codemirror_ver = 5.8.0

tinymce:
	curl -L -O http://download.moxiecode.com/tinymce/$(tinymce3_zip)
	unzip $(tinymce3_zip)
	rm -rf static/js/tinymce3
	mv tinymce/jscripts/tiny_mce static/js/tinymce3
	rm -rf $(tinymce3_zip) tinymce

	curl -L -O http://download.moxiecode.com/tinymce/$(tinymce4_zip)
	unzip $(tinymce4_zip)
	rm -rf static/js/tinymce4
	mv tinymce/js/tinymce static/js/tinymce4
	rm -rf $(tinymce4_zip) tinymce

codemirror:
	curl -L -O https://github.com/codemirror/CodeMirror/archive/$(codemirror_ver).zip
	unzip $(codemirror_ver).zip
	rm -rf static/js/codemirror
	mkdir static/js/codemirror
	mv CodeMirror-$(codemirror_ver)/addon static/js/codemirror
	mv CodeMirror-$(codemirror_ver)/keymap static/js/codemirror
	mv CodeMirror-$(codemirror_ver)/lib static/js/codemirror
	mv CodeMirror-$(codemirror_ver)/mode static/js/codemirror
	mv CodeMirror-$(codemirror_ver)/theme static/js/codemirror
	rm -rf $(codemirror_ver).zip CodeMirror-$(codemirror_ver)
