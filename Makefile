update_conf: 
	./build_utils/gen-pyproject.sh
	# ./build_utils/gen-setup.sh

test:update_conf remove_test
	coverage run -m pytest
	coverage html -d html_coverage

build_no_test: remove_build
	python -m build .

remove_test:
	rm -rf .pytest_cache/
	rm -rf sh_crypt/__pycache__/
	rm -rf sh_crypt/tests/__pycache__/
	rm -rf .tox/
	rm -f .coverage
	rm -rf html_coverage/
		
remove_build:
	rm -rf dist/
	rm -rf build/
	rm -rf sh_crypt.egg-info/
	rm -rf sh_crypt/sh_crypt.egg-info
	
		
build: remove_build test
	python -m build .
	tox

install_and_test:
	python setup.py install 
	python demo/demo.py

tag: build
	bash build_utils/git-tag.sh

deploy_test:
	twine upload -r testpypi dist/* --verbose
	
deploy_prod:
	twine upload dist/*