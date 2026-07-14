.PHONY: test package clean help

help:
	@echo "Targets: test | package | clean"

test:
	python3 -m unittest discover -s tests -v

package:
	./package.sh

clean:
	rm -f "Multiline to Single.alfredworkflow" Multiline.to.Single.alfredworkflow
	rm -rf __pycache__ tests/__pycache__ .pytest_cache
