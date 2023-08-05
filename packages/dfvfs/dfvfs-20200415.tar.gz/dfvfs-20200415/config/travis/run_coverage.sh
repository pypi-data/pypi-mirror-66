#!/bin/bash
#
# Script to run Python 3 with code coverage tests on Travis-CI.
#
# This file is generated by l2tdevtools update-dependencies.py, any dependency
# related changes should be made in dependencies.ini.

# Exit on error.
set -e;

COVERAGE="/usr/bin/coverage";

if ! test -x "${COVERAGE}" && test -x "/usr/bin/python-coverage";
then
	# Ubuntu has renamed coverage but codecov.sh depends on /usr/bin/coverage
	ln -s /usr/bin/python-coverage /usr/bin/coverage;
fi
curl -o codecov.sh -s https://codecov.io/bash;

${COVERAGE} erase;

${COVERAGE} run --source=dfvfs --omit="*_test*,*__init__*,*test_lib*" ./run_tests.py;

/bin/bash ./codecov.sh;

if test -f tests/end-to-end.py;
then
	PYTHONPATH=. python3 ./tests/end-to-end.py --debug -c config/end-to-end.ini;
fi

python3 ./setup.py build

python3 ./setup.py sdist

python3 ./setup.py bdist

python3 ./setup.py install
