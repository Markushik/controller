.ONESHELL:

py := poetry run

package_dir := ./app/
code_dir := $(package_dir)

.PHONY: checks
checks:
	$(py) flake8 $(code_dir)
