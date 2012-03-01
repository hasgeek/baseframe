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
	cd baseframe; make tinymce
