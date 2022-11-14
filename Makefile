migrate: run-dependecies
	docker-compose exec api python manage.py migrate --noinput
	docker-compose exec authenticator python manage.py migrate --noinput

	docker-compose exec api python manage.py loaddata fixtures/dump.json --app product --app product_cost --app events --app auth.user
	docker-compose exec authenticator python manage.py loaddata fixtures/dump.json --app auth.user

test: run-dependecies
	bash test_runner.sh

run-dependecies:
	docker-compose -f docker-compose-dependecies.yml up -d

run: run-dependecies
	docker-compose up -d

logs:
	docker-compose logs -f

down:
	docker-compose down

down-dependecies:
	docker-compose -f docker-compose-dependecies.yml down
