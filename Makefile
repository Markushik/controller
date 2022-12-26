.ONESHELL:

py := poetry run

package_dir := ./backend/
code_dir := $(package_dir)

.PHONY: auto_refact
auto_refact:
	$(py) isort $(code_dir)

.PHONY: checks
checks:
	$(py) flake8 $(code_dir)
