run:
	docker compose -f deployment/docker-compose.yml up --build

clean:
	docker compose -f deployment/docker-compose.yml down
	rm -rf logs/

test:
	python -m unittest discover tests/