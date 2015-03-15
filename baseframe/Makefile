# Makefile for tinymce
all: tinymce codemirror

tinymce3_zip = tinymce_3.5.11_jquery.zip
tinymce4_zip = tinymce_4.1.7_jquery.zip
codemirror_zip = codemirror.zip

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
	curl -L -O http://codemirror.net/$(codemirror_zip)
	unzip $(codemirror_zip)
	rm -rf static/js/codemirror
	mkdir static/js/codemirror
	mv codemirror-*/addon static/js/codemirror
	mv codemirror-*/keymap static/js/codemirror
	mv codemirror-*/lib static/js/codemirror
	mv codemirror-*/mode static/js/codemirror
	mv codemirror-*/theme static/js/codemirror
	rm -rf $(codemirror_zip) codemirror-*
