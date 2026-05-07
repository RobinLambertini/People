.PHONY: lint fix check serve

JSON_FILE := guests.json
PORT ?= 8080

lint:
	@echo "Linting $(JSON_FILE)..."
	@jq empty $(JSON_FILE) && echo "JSON is valid" || exit 1

fix:
	@echo "Formatting $(JSON_FILE)..."
	@jq . $(JSON_FILE) > $(JSON_FILE).tmp && mv $(JSON_FILE).tmp $(JSON_FILE)
	@echo "Done."

check: lint

serve:
	@echo "Serving on http://localhost:$(PORT)"
	@python3 -m http.server $(PORT)
