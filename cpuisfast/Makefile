all: build dev

build:
	npx tailwindcss -i style.css -o ./dist/style.css
	python3 main.py

dev:
	xdg-open dist/index.html
