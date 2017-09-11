.PHONY: help install install-dev assets clean delpyc syncf5
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

print("Please use `make <target>` where <target> is one of these")
for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

delpyc: ## to remove all *.pyc files, this is recursive from the current directory
	find . -name "*\.pyc"|xargs rm -f

clean: delpyc ## to clean your local repository from all builded stuff and caches
	rm -Rf bin include lib local node_modules compass/.sass-cache

install: ## to build the project
	virtualenv --no-site-packages .
	bin/pip install gunicorn
	bin/pip install -r pip-requirements/basic.txt
	bin/python manage.py migrate

install-dev: install ## to build the project for development
	bundle install --gemfile=compass/Gemfile
	npm install
	foundation new foundation5 --version=5.5.2

assets: ## to build assets for production environment
	grunt uglify
	grunt cssmin

syncf5: ## to synchronize Foundation5 sources dir to assets (used only when you upgrade Foundation5)
	rm -f foundation5/bower_components/foundation/js/vendor/jquery.js
	cp foundation5/bower_components/jquery/dist/jquery.js foundation5/bower_components/foundation/js/vendor/jquery.js
	rm -Rf project/webapp_statics/js/foundation5
	cp -r foundation5/bower_components/foundation/js project/webapp_statics/js/foundation5
	# Cleaning vendor libs
	rm -Rf project/webapp_statics/js/foundation5/vendor
	mkdir -p project/webapp_statics/js/foundation5/vendor
	# Getting the real sources for updated vendor libs
	cp foundation5/bower_components/fastclick/lib/fastclick.js project/webapp_statics/js/foundation5/vendor/
	cp foundation5/bower_components/foundation/js/vendor/jquery.js project/webapp_statics/js/foundation5/vendor/
	cp foundation5/bower_components/jquery-placeholder/jquery.placeholder.js project/webapp_statics/js/foundation5/vendor/
	cp foundation5/bower_components/jquery.cookie/jquery.cookie.js project/webapp_statics/js/foundation5/vendor/
	cp foundation5/bower_components/modernizr/modernizr.js project/webapp_statics/js/foundation5/vendor/
