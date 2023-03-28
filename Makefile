#   -------------------------------------------------------------
#   Resolve hash
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Project:        Nasqueron
#   License:        BSD-2-Clause
#   -------------------------------------------------------------

RMDIR=rm -rf
PYTHON=python
DISCOVER_TESTS=$(PYTHON) -m unittest discover
REFORMAT=black

#   -------------------------------------------------------------
#   Main targets
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

all:

package: dist

clean: clean-package

test:
	${DISCOVER_TESTS} tests/

#   -------------------------------------------------------------
#   Development helpers
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

reformat:
	find bin -type f | xargs ${REFORMAT}
	find src -type f -name '*.py' | xargs ${REFORMAT}
	find tests -type f -name '*.py' | xargs ${REFORMAT}

#   -------------------------------------------------------------
#   Packaging targets
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

dist:
	${PYTHON} -m build

clean-package:
	${RMDIR} dist src/resolve_hash.egg-info
