SHELL:=/bin/bash
PYTHONPATH:=..:.
PATH := venv/bin:$(PATH)
PYTHON	= PYTHONPATH=..:. venv/bin/python
PYDIRCHK= 'import sys; print(sys.prefix)'
PYDIR	= $(shell ${PYTHON} -c ${PYDIRCHK})
PYBIN	= ${PYDIR}/bin
PYVERCHK= 'import sys; print sys.version[:3]'
PYVER	= $(shell ${PYTHON} -c ${PYVERCHK})
PYCC	= ${PYDIR}/lib/python${PYVER}/compileall.py
SRC_DIR	= .
LINTRC  = .pylintrc


setup: cleanall venv libraries

all: cleanall venv libraries sloc test flakes lint

cleanall: cleanvenv clean
cleanvenv:
	rm -Rf venv

clean:
	for file in `find . -name "*.py[co]" -print -o -name "*~" -print -o -name ".#*" -print`; do echo $$file; rm $$file; done
	rm -f pyflakes.log
	rm -f pylint.log
	rm -f sloccount.sc
	rm -f output.xml
	rm -f coverage.xml
	rm -f xunit.xml
	rm -f .coverage
	rm -Rf htmlcov/
	rm -Rf sphinx/_source/
	rm -Rf sphinx/_build/

venv: venv/bin/activate
venv/bin/activate:
	test -d venv || virtualenv -p /usr/bin/python3 venv

libraries:
	venv/bin/pip install -Ur requirements.txt


audit: venv sloc test flakes lint docs

sloc: venv
	sloccount --duplicates --wide --details $(SRC_DIR) | fgrep -v .git | fgrep -v venv | fgrep -v tests > sloccount.sc || :

test: venv
	${PYTHON} manage.py test -v 2 || :
	${PYBIN}/coverage html

flakes: venv
	find $(SRC_DIR) -name "*.py" | egrep -v '^./tests/' | egrep -v '^./venv/' | xargs ${PYBIN}/pyflakes > pyflakes.log || :

lint: venv
	find $(SRC_DIR) -name "*.py" | egrep -v '^./tests/' | egrep -v '^./venv/' | xargs ${PYBIN}/pylint --output-format=parseable --rcfile=${LINTRC} --reports=y > pylint.log || :

run: venv
	${PYTHON} manage.py runserver
