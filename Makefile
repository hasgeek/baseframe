# Makefile for sass and less stylesheets
all: css

css: sass less

sass:
	# Compass config is in config.rb
	compass compile

less:
	lessc baseframe/static/less/bootstrap/bootstrap.less baseframe/static/css/bootstrap.css
	lessc baseframe/static/less/bootstrap/responsive.less baseframe/static/css/responsive.css

tinymce:
	wget http://github.com/downloads/tinymce/tinymce/tinymce_3.4.9_jquery.zip
	unzip tinymce_3.4.9_jquery.zip
	mv tinymce/jscripts/tiny_mce baseframe/static/js
	rm -rf tinymce_3.4.9_jquery.zip tinymce
