.ONESHELL:

py := poetry run

package_dir := ./backend/
code_dir := $(package_dir)

.PHONY: checks
checks:
	$(py) isort $(code_dir)
	$(py) flake8 $(code_dir)