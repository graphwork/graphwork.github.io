.PHONY: screencast dev build

screencast:
	./screencasts/record.sh
	cp screencasts/demo.gif screencasts/demo.webm public/

dev:
	npm run dev

build:
	npm run build
