dist: *.js package*.json cldr-coverage.py
	npm run package
	cp cldr-coverage.py dist/cldr-coverage.py

update:
	npm update

dev-update:
	npm update --dev

.PHONY: dev-update update