# Makefile for tinymce
all: tinymce

tinymce3_zip = tinymce_3.5.10_jquery.zip
tinymce4_zip = tinymce_4.0.26_jquery.zip

tinymce:
	curl -L -O http://github.com/downloads/tinymce/tinymce/$(tinymce3_zip)
	unzip $(tinymce3_zip)
	rm -rf static/js/tinymce3
	mv tinymce/jscripts/tiny_mce static/js/tinymce3
	rm -rf $(tinymce3_zip) tinymce

	curl -L -O http://download.moxiecode.com/tinymce/$(tinymce4_zip)
	unzip $(tinymce4_zip)
	rm -rf static/js/tinymce4
	mv tinymce/js/tinymce static/js/tinymce4
	rm -rf $(tinymce4_zip) tinymce
